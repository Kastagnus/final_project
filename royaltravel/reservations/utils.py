from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# ფუნქცია რომელსაც ვიძახებთ რეზერვაციის მოდელში, აგენერირებს პდფ ფაილს და გადასაცემს რეზერვაციის დეტალებს
def generate_reservation_pdf(reservation):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setLineWidth(.3)
    c.setFont('Helvetica', 12)

    c.drawString(30, 750, 'Reservation Confirmation')
    c.drawString(30, 735, f'Reservation Number: {reservation.reservation_reference}')
    c.drawString(30, 720, f'Full Name: {reservation.full_name}')
    c.drawString(30, 705, f'Tour: {reservation.tour.title}')
    c.drawString(30, 690, f'Start Date: {reservation.start_date}')
    c.drawString(30, 675, f'End Date: {reservation.end_date}')
    c.drawString(30, 660, f'Number of People: {reservation.number_of_people}')
    c.drawString(30, 645, f'Total Price: ${reservation.total_price}')
    c.drawString(30, 630, f'Itinerary: {reservation.tour.description}')

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer