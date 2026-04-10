# encoding:utf-8
from gramps.gen.plug import Gramplet


class CompletenessGramplet(Gramplet):

    def init(self):
        self.set_text("Загрузка...")

    def db_changed(self):
        self.connect(self.dbstate.db, "person-rebuild", self.update)

    def main(self):
        self.set_text("Gramplet работает!\n")
        yield False
