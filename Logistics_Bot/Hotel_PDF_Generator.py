import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class HotelPDFGenerator:
    def __init__(self, data):
        self.data = data
        self.top_5_hotels = data['data']['results']['hotelCards'][:5]
        self.file_path = "Hotel_Data.pdf"
        self.width, self.height = letter

    def draw_hotel_info(self, c, hotel, y_pos):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, y_pos, hotel['name'])
        c.setFont("Helvetica", 12)
        c.drawString(30, y_pos - 20, f"Stars: {hotel['stars']}")
        c.drawString(200, y_pos - 20, f"Distance: {hotel['distance']}")
        c.drawString(30, y_pos - 40, f"Rating: {hotel['reviewsSummary']['score']} ({hotel['reviewsSummary']['scoreDesc']})")
        c.drawString(200, y_pos - 40, f"Reviews: {hotel['reviewsSummary']['total']}")
        c.drawString(30, y_pos - 60, f"Lowest Price: {hotel['lowestPrice']['price']}")
        y_pos -= 80
        return y_pos

    def generate_pdf(self):
        c = canvas.Canvas(self.file_path, pagesize=letter)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, self.height - 30, "Top 5 Hotel Results")

        y_position = self.height - 60

        for hotel in self.top_5_hotels:
            y_position = self.draw_hotel_info(c, hotel, y_position)
            if y_position < 60:  # Check if there's enough space left on the page
                c.showPage()  # Create a new page if not
                y_position = self.height - 30  # Reset position

        c.save()
        print(f"PDF file created successfully: {self.file_path}")


# # Example usage (in another script):
# if __name__ == "__main__":
#     # Assuming you have 'data.json' in the same directory
#     with open('data.json', 'r') as file:
#         data = json.load(file)

#     pdf_generator = HotelPDFGenerator(data)
#     pdf_generator.generate_pdf()