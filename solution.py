# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14   # 대출 기간
MAX_LOANS = 3    # 1인 최대 대출 권수


def _valid_day(day):
    # 1 이상의 정수만 허용 (True/False는 정수로 보지 않음)
    return isinstance(day, int) and not isinstance(day, bool) and day >= 1


class LibraryLoan:
    def __init__(self):
        self.loans = {}         # book_id -> {"name", "day", "due"}  (지금 빌려 간 책)
        self.blocked = {}       # name -> [(정지 시작일, 정지 마지막 날), ...]
        self.history = []       # 지금까지의 대출·반납 기록

    def borrow(self, book_id, name, day):
        if not isinstance(book_id, str) or book_id not in BOOKS:
            return False                      # 1. 없는 책 번호
        if not _valid_day(day):
            return False                      # 2. 잘못된 날짜
        if book_id in self.loans:
            return False                      # 3. 이미 대출 중
        mine = [l for l in self.loans.values() if l["name"] == name]
        if len(mine) >= MAX_LOANS:
            return False                      # 4. 이미 3권
        if any(day > l["due"] for l in mine):
            return False                      # 5. 기한 지난 책을 갖고 있음
        if any(start <= day <= end for start, end in self.blocked.get(name, [])):
            return False                      # 6. 대출 정지 기간

        due = day + LOAN_DAYS
        self.loans[book_id] = {"name": name, "day": day, "due": due}
        self.history.append(("borrow", book_id, name, day))
        return True

    def return_book(self, book_id, name, day):
        loan = self.loans.get(book_id) if isinstance(book_id, str) else None
        if loan is None or loan["name"] != name:
            return -1                         # 그 사람이 빌리고 있지 않음
        if not _valid_day(day):
            return -1                         # 잘못된 날짜
        if day < loan["day"]:
            return -1                         # 빌린 날보다 이른 날짜

        late = max(0, day - loan["due"])
        if late > 0:
            # 반납한 날부터 연체 일수만큼 정지 (예: 30일째 3일 연체 → 30~32일째).
            # 기간이 겹치면 합쳐질 뿐 더해지지 않으므로, 더 늦게 끝나는 쪽까지 막힘
            self.blocked.setdefault(name, []).append((day, day + late - 1))

        del self.loans[book_id]
        self.history.append(("return", book_id, name, day))
        return late

    def get_loans(self, name):
        mine = [(b, l["due"]) for b, l in self.loans.items() if l["name"] == name]
        return sorted(mine, key=lambda x: (x[1], x[0]))
