# encoding:utf-8
from gramps.gen.plug import Gramplet


class CompletenessGramplet(Gramplet):

    def init(self):
        self.set_text("Нет данных")

    def db_changed(self):
        self.connect(self.dbstate.db, "person-add", self.update)
        self.connect(self.dbstate.db, "person-update", self.update)
        self.connect(self.dbstate.db, "person-delete", self.update)
        self.connect(self.dbstate.db, "person-rebuild", self.update)

    def main(self):
        db = self.dbstate.db
        total = db.get_number_of_people()

        if total == 0:
            self.set_text("База данных пуста\n")
            yield False
            return

        self.set_text("Всего персон: %d\n" % total)
        yield False
