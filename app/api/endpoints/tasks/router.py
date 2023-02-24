
from fastapi import APIRouter, BackgroundTasks, Depends

from app.api.endpoints.auth.utils import get_current_user

from app.api.endpoints.tasks.tasks import send_email_report_dashboard
# from app.api.endpoints.tasks.tasks2 import send_email_async

router = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    # 1400 ms - Клиент ждет
    # send_email_report_dashboard(user.id)
    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    #background_tasks.add_task(send_email_report_dashboard, user.username)
    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    send_email_report_dashboard.delay(user.email)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }
