# encoding:utf-8
from gramps.gen.plug import Gramplet
from gramps.gen.display.name import displayer as name_displayer

_TOP_N = 10


class CompletenessGramplet(Gramplet):

    def init(self):
        self.set_use_markup(True)
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

        counts = {"birth_date": 0, "death_date": 0, "birth_place": 0, "photo": 0}
        person_scores = []

        for handle in handles:
            yield True
            person = db.get_person_from_handle(handle)
            missing = 0

            birth_ref = person.get_birth_ref()
            if birth_ref:
                ev = db.get_event_from_handle(birth_ref.ref)
                if ev.get_date_object().is_empty():
                    counts["birth_date"] += 1
                    missing += 1
                if not ev.get_place_handle():
                    counts["birth_place"] += 1
                    missing += 1
            else:
                counts["birth_date"] += 1
                counts["birth_place"] += 1
                missing += 2

            death_ref = person.get_death_ref()
            if death_ref:
                ev = db.get_event_from_handle(death_ref.ref)
                if ev.get_date_object().is_empty():
                    counts["death_date"] += 1
                    missing += 1
            else:
                counts["death_date"] += 1
                missing += 1

            if not person.get_media_list():
                counts["photo"] += 1
                missing += 1

            name = name_displayer.display(person)
            person_scores.append((missing, name or "Без имени", handle))

        person_scores.sort(reverse=True)

        fields = [
            ("Дата рождения",  counts["birth_date"]),
            ("Дата смерти",    counts["death_date"]),
            ("Место рождения", counts["birth_place"]),
            ("Фото",           counts["photo"]),
        ]

        self.set_text("")
        self.render_text("<b>Полнота базы данных</b>\n\n")
        self.append_text("Всего персон: %d\n\n" % total)
        self.render_text("<b>Отсутствующие данные:</b>\n")
        w = len(str(total))
        for label, count in fields:
            pct = 100 * count // total
            self.append_text("  %-17s %3d%% (%*d/%d)\n" % (label + ":", pct, w, count, total))

        self.append_text("\n")
        self.render_text("<b>Топ-%d самых неполных персон:</b>\n" % _TOP_N)
        for i, (missing, name, handle) in enumerate(person_scores[:_TOP_N], 1):
            self.append_text("  %d. " % i)
            self.link(name, "Person", handle)
            self.append_text(" (%d/4)\n" % (4 - missing))

        self.append_text("", scroll_to="begin")
        yield False
