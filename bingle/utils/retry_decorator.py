from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from bingle.exception import APILimitError


# Retry Decorator 정의
def retry_on_exception(max_attempts=10, wait_time=2):
    """
    함수 호출에 실패했을 때, 재시도하는 데코레이터 함수.
    :param max_attempts: 최대 재시도 횟수
    :param wait_time: 재시도 간 대기 시간 (지수적 증가 사용)
    """
    return retry(
        reraise=True,  # 마지막 exception을 그대로 raise
        stop=stop_after_attempt(max_attempts),  # 최대 재시도 횟수
        wait=wait_exponential(multiplier=wait_time, min=wait_time, max=60),  # 지수적 증가 대기
        retry=retry_if_exception_type(APILimitError),  # 재시도할 예외 타입
    )
