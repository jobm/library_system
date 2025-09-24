from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
import logging
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def remind_overdue_books():
    try:
        logger.info(f"trying to senf reminder for due loan")
        today = datetime.now() + timedelta(day=14)
        loans = Loan.objects.filter(due_date__gte=today, is_returned=False)

        for loan in loans:
            send_mail(
                subject='Book Is Overdue',
                message=f"""
                Hello {loan.member.user.username},\n\n
                Book {loan.book.title} that you borrowed on {loan.loan_date} is overdue.\n
                Please return it.\n 
                It was due on {loan.due_date}.
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[loan.member.user.email],
                fail_silently=False,
            )
            logger.info(f"reminder sent for loan {loan.id} on {loan.due_date}")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
