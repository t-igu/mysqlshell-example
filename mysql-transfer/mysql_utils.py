import yaml
import os
import shutil
import subprocess

from loguru import logger

from mylogger import setup_logger

_ROOT_DIR = os.getcwd()

class MySQLTransfer:
    def load_settings(self) -> dict:
        # 設定ファイルを読み込み
        config_path = os.path.join(_ROOT_DIR, 'config', 'settings.yaml')
        with open(config_path, 'r') as yml:
            config = yaml.safe_load(yml)
            return config

    def get_url(self, user, passwd, host, port, schema) -> str:
        # MySQL Shell への接続URL
        base_cmd = f'{user}:{passwd}@{host}:{port}/{schema}'
        return base_cmd

    def __init__(self) -> None:
        # dump用のテンポラリフォルダを初期化する
        self._dumpdir = os.path.join(_ROOT_DIR, 'dumps').replace("\\", "/")
        if os.path.exists(self._dumpdir):
            shutil.rmtree(self._dumpdir)
        os.mkdir(self._dumpdir)

        # 設定ファイル(yaml)を読み込んでパラメータにセットする
        config = self.load_settings()

        # ログをセットアップする
        setup_logger(
            config['log']['filepath'],
            config['log']['rotation'],
            config['log']['retention'],
        )

        # setup dump-tables utility params
        url = self.get_url(
            config['dump']['user'],
            config['dump']['passwd'],
            config['dump']['host'],
            config['dump']['port'],
            config['load']['schema'],
        )
        self.dump_cmd = f"mysqlsh {url} -- util dump-tables {config['dump']['schema']}"
        self.dump_tables = config['dump']['tables']
        self.dump_option = ' '.join(config['dump']['options']) if config['dump']['options'] else ''

        # setup load-dump utility params
        url = self.get_url(
            config['load']['user'],
            config['load']['passwd'],
            config['load']['host'],
            config['load']['port'],
            config['load']['schema'],
        )
        self.load_cmd = f"mysqlsh {url} -- util load-dump"
        load_option =[f"--{load_option}" for load_option in config['load']['options']]
        self.load_option = ' '.join(load_option)

    @logger.catch            
    def exec_cmd(self, cmd):
        output = subprocess.run(cmd)
        if output==0:
            return output
        else:
            raise Exception(f'command execute error! cmd={cmd}')

    def create_dump_cmd(self, table_name):
        cmd = f'{self.dump_cmd} {table_name} --output-url {self._dumpdir}/{table_name} {self.dump_option}'
        return cmd

    def create_load_cmd(self, table_name):
        cmd = f'{self.load_cmd} {self._dumpdir}/{table_name} {self.load_option}'
        return cmd

    def exec_transfer(self, table_name):
            dumpcmd = self.create_dump_cmd(table_name)
            loadcmd = self.create_load_cmd(table_name)
            ret = self.exec_cmd(dumpcmd)
            logger.info(f'result={ret} {dumpcmd}')
            if ret==0:
                ret2 = self.exec_cmd(loadcmd)
                logger.info(f'result={ret2} {loadcmd}')
    def transfer(self) -> None:
        for table_name in self.dump_tables:
            try:
                logger.info(f'transfer start. table={table_name}')
                ret = self.exec_transfer(table_name)
            except subprocess.CalledProcessError as e:
                msg = f"transfer failed table:{table_name} returncode:{e.returncode}, output:{e.output}"
        if os.path.exists(self._dumpdir):
            shutil.rmtree(self._dumpdir)

if __name__ == '__main__':
    trans = MySQLTransfer()
    trans.transfer()
