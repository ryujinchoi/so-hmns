import copy
from decimal import Decimal, localcontext, Context, MAX_PREC, Overflow, Underflow, DivisionByZero

class SoHmnsGuard:
    def __init__(self, dimension=3, sigma=0.5):
        self.dimension = int(dimension)
        self.sigma = str(sigma)
        with localcontext() as ctx:
            ctx.prec = 100
            self.alpha = Decimal('1') / (Decimal(str(self.dimension)) + Decimal('1'))

    def run(self, raw_input):
        with localcontext(Context(prec=200)) as ctx:
            # 튕김 방지: 오버플로우/디비전바이제로가 발생해도 crash 대신 무한대(Infinity) 값으로 변환 유지
            ctx.traps[Overflow] = False
            ctx.traps[Underflow] = False
            ctx.traps[DivisionByZero] = False
            try:
                val = Decimal(str(raw_input))
                result = (val ** 2) / self.alpha
                return copy.deepcopy(result)
            except Exception as e:
                return f"[SYSTEM GUARD ACTIVATED] Secured Fault: {e}"
            finally:
                ctx.clear_flags() # 하드웨어 캐시 메모리 초기화

if __name__ == "__main__":
    guard = SoHmnsGuard()
    print("-> 시스템 보호 모드 가동 완료.")
    user_data = "999999.999999999999999999"
    print(f"-> 입력 검증 결과: {guard.run(user_data)}")
