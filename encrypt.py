from __future__ import annotations

import getpass
import pathlib

import paramiko
from cryptography.fernet import Fernet
from pydantic import BaseModel, SecretStr, validator


class Account(BaseModel):

    hostname: str
    username: str
    password: SecretStr

    class Config:
        allow_mutation = False
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }

    @validator("*", pre=True, always=True)
    def not_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("Empty strings are not allowed.")
        return v

    @validator("hostname", "username", always=True)
    def not_contain_space(cls, v: str) -> str:
        if " " in v:
            raise ValueError("space are not allowed.")
        return v

    @classmethod
    def get_account(
        cls, hostname: str, username: str, password: str
    ) -> Account:
        password_encrypted = Account.encrypt(password)
        account = Account(
            hostname=hostname,
            username=username,
            password=SecretStr(password_encrypted),
        )
        return account

    @classmethod
    def get_account_from_file(cls, file: pathlib.Path) -> Account:
        if not file.exists():
            Account.make_account_file(file)
        return Account.parse_file(file)

    @classmethod
    def make_account_file(cls, file: pathlib.Path) -> None:

        hostname = input("ホスト名入力:")
        username = input("ユーザ名入力:")
        password = getpass.getpass(prompt="パスワード入力:")

        account = Account(
            hostname=hostname,
            username=username,
            password=SecretStr(Account.encrypt(password)),
        )

        file = pathlib.Path(file)
        file.write_text(account.json())

    def connect(self, ssh: paramiko.SSHClient) -> None:

        ssh.connect(
            hostname=self.hostname,
            username=self.username,
            password=Account.decrypt(self.password.get_secret_value()),
        )
