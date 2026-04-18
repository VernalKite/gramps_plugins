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
            if birth_ref:
                ev = db.get_event_from_handle(birth_ref.ref)
                if ev.get_date_object().is_empty():
                    no_birth_date += 1
                if not ev.get_place_handle():
                    no_birth_place += 1
            else:
                no_birth_date += 1
                no_birth_place += 1  # если нет события рождения — место тоже неизвестно

            death_ref = person.get_death_ref()
            if not death_ref:
                no_death_date += 1
            else:
                ev = db.get_event_from_handle(death_ref.ref)
                if ev.get_date_object().is_empty():
                    no_death_date += 1

            if not person.get_media_list():
                no_photo += 1

        _BAR_WIDTH = 20
        fields = [
            ("Дата рождения",  no_birth_date),
            ("Дата смерти",    no_death_date),
            ("Место рождения", no_birth_place),
            ("Фото",           no_photo),
        ]

        self.set_text("")
        self.append_text("Всего персон: %d\n\n" % total)
        self.append_text("Отсутствующие данные:\n")
        for label, count in fields:
            pct = 100 * count // total
            bar = "█" * (pct * _BAR_WIDTH // 100)
            self.append_text("  %-17s %3d%%  %s\n" % (label + ":", pct, bar))
        # второй проход — считаем пропуски по каждой персоне отдельно
        person_data = []
        for handle in handles:
            yield True
            person = db.get_person_from_handle(handle)
            miss = 0

            birth_ref = person.get_birth_ref()
            if birth_ref:
                ev = db.get_event_from_handle(birth_ref.ref)
                if ev.get_date_object().is_empty():
                    miss += 1
                if not ev.get_place_handle():
                    miss += 1
            else:
                miss += 2

            death_ref = person.get_death_ref()
            if not death_ref:
                miss += 1
            else:
                ev = db.get_event_from_handle(death_ref.ref)
                if ev.get_date_object().is_empty():
                    miss += 1

            if not person.get_media_list():
                miss += 1

            pname = person.get_primary_name()
            name = ("%s %s" % (pname.get_first_name(), pname.get_surname())).strip()
            person_data.append((miss, name or "Без имени", handle))

        person_data.sort(reverse=True)

        self.append_text("\nТоп-10 самых неполных персон:\n")
        for i, (miss, name, _handle) in enumerate(person_data[:10], 1):
            self.append_text("  %d. %s (%d/4)\n" % (i, name, 4 - miss))

        self.append_text("", scroll_to="begin")
        yield False
