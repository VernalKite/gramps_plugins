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
        self.set_text("Считаю...\n")
        yield True

        db = self.dbstate.db
        handles = db.get_person_handles()
        total = len(handles)

        if total == 0:
            self.set_text("База данных пуста\n")
            yield False
            return

        no_birth_date = 0
        no_death_date = 0
        no_birth_place = 0
        no_photo = 0

        for handle in handles:
            yield True
            person = db.get_person_from_handle(handle)

            birth_ref = person.get_birth_ref()
            if not birth_ref:
                no_birth_date += 1
            else:
                ev = db.get_event_from_handle(birth_ref.ref)
                if ev.get_date_object().is_empty():
                    no_birth_date += 1
                if not ev.get_place_handle():
                    no_birth_place += 1

            death_ref = person.get_death_ref()
            if not death_ref:
                no_death_date += 1
            else:
                ev = db.get_event_from_handle(death_ref.ref)
                if ev.get_date_object().is_empty():
                    no_death_date += 1

            if not person.get_media_list():
                no_photo += 1

        self.set_text("")
        self.append_text("Всего персон: %d\n\n" % total)
        self.append_text("Без даты рождения:  %d (%.0f%%)\n" % (no_birth_date,  100 * no_birth_date  / total))
        self.append_text("Без даты смерти:    %d (%.0f%%)\n" % (no_death_date,  100 * no_death_date  / total))
        self.append_text("Без места рождения: %d (%.0f%%)\n" % (no_birth_place, 100 * no_birth_place / total))
        self.append_text("Без фото:           %d (%.0f%%)\n" % (no_photo,       100 * no_photo       / total))
        self.append_text("", scroll_to="begin")
        yield False
