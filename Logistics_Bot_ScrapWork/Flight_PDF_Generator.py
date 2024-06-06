import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ItineraryPDFGenerator:
    def __init__(self, data):
        self.data = data
        self.styles = getSampleStyleSheet()

    def format_to_flowables(self, itineraries):
        flowables = [Paragraph("# Top 5 Itineraries", self.styles['Title']), Spacer(1, 12)]
        
        for itinerary in itineraries[:5]:  # Limit to top 5
            flowables.append(Paragraph(f"## Itinerary ID: {itinerary['id']}", self.styles['Heading2']))
            flowables.append(Spacer(1, 12))
            
            # Add Price
            flowables.append(Paragraph(f"**Price:** {itinerary['price']['formatted']}", self.styles['Normal']))
            flowables.append(Spacer(1, 12))
            
            for leg in itinerary['legs']:
                flowables.append(Paragraph(f"### Leg ID: {leg['id']}", self.styles['Heading3']))
                flowables.append(Spacer(1, 8))
                
                leg_info = [
                    ['Origin', f"{leg['origin']['name']} ({leg['origin']['displayCode']})"],
                    ['Destination', f"{leg['destination']['name']} ({leg['destination']['displayCode']})"],
                    ['Departure', leg['departure']],
                    ['Arrival', leg['arrival']],
                    ['Duration', f"{leg['durationInMinutes']} minutes"],
                    ['Carrier', leg['carriers']['marketing'][0]['name']]
                ]
                
                table = Table(leg_info, colWidths=[100, 300])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                ]))
                
                flowables.append(table)
                flowables.append(Spacer(1, 12))
                
        return flowables

    def generate_pdf(self, filename="Flight_Data.pdf"):
        # Extracting itineraries from the data
        itineraries = self.data['data']['itineraries']

        # Format to flowable elements
        flowables = self.format_to_flowables(itineraries)

        # Set up the PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter)
        
        # Build the PDF document
        doc.build(flowables)

        print('PDF file has been created successfully.')

# Example usage:
# if __name__ == "__main__":
#     with open('flight.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#     generator = ItineraryPDFGenerator(data)
#     generator.generate_pdf("itineraries.pdf")