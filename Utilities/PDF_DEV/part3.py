from fpdf import FPDF

class Info(FPDF):
    @staticmethod
    def header(pdf):
        # Logo
        pdf.image('Assets/mef logo.png', 10, 8, 25)
        # User Image (Right aligned)
        pdf.image('Assets/woman.png', pdf.w - 35, 4, 23)
        
        # Title
        title = 'Transcript Document'
        # Font for title
        pdf.set_font('helvetica', 'B', 15)
        # Calculate width of the title and position
        title_w = pdf.get_string_width(title) + 6
        doc_w = pdf.w
        pdf.set_x((doc_w - title_w) / 2)
        # Title
        pdf.cell(title_w, 10, title, border=False, ln=1, align='C')

        # Line break
        pdf.ln(12)

        # Student Information Table
        student_info_labels = ['Student ID', 'Name', 'Faculty/Department', 'Language of Instruction']
        student_info_values = ['041901024', 'TUANA SELEN', 'Faculty of Engineering / Computer Engineering', 'English']
        additional_info_labels = ['National ID', 'Surname', 'Program Name', 'Student Status']
        additional_info_values = ['33760786358', 'ÖZHAZDAY', 'Computer Engineering', 'Continuing']

        col_widths = [32, 85, 28, 45] # column widths

        for i in range(4):
            pdf.set_font('helvetica', '', 8)
            pdf.cell(col_widths[0], 7, student_info_labels[i], 1, 0, 'L')
            pdf.set_font('helvetica', 'B', 8)
            pdf.cell(col_widths[1], 7, student_info_values[i], 1, 0, 'L')
            pdf.set_font('helvetica', '', 8)
            pdf.cell(col_widths[2], 7, additional_info_labels[i], 1, 0, 'L')
            pdf.set_font('helvetica', 'B', 8)
            pdf.cell(col_widths[3], 7, additional_info_values[i], 1, 1, 'L')

        pdf.ln(12) # Line break after the table


class Original(FPDF):
    @staticmethod
    def create_table(pdf):
        # Set font for table header
        pdf.set_font('helvetica', 'B', 8)

        # Set column widths
        col_widths = [25, 85, 25, 15, 15, 25]

        # Add new merged row
        total_width = sum(col_widths)
        pdf.set_font('helvetica', 'B', 10)
        pdf.set_fill_color(192, 192, 192)  # Set fill color for new row
        pdf.cell(total_width, 7, '2020-2021 Fall Semester', 1, 1, 'C', 1)  # Merge cells

        # Set fill color for header row
        pdf.set_fill_color(255, 255, 255)  # Set to white for other rows
        # Set font size to 8 for other headers
        pdf.set_font('helvetica', 'B', 8)
        
        # Add table header
        pdf.cell(col_widths[0], 6, 'Course Code', 1, 0, 'L')
        pdf.cell(col_widths[1], 6, 'Course Name', 1, 0, 'L')
        pdf.cell(col_widths[2], 6, 'Language', 1, 0, 'L')
        pdf.cell(col_widths[3], 6, 'ECTS', 1, 0, 'L')
        pdf.cell(col_widths[4], 6, 'Grade', 1, 0, 'L')
        pdf.cell(col_widths[5], 6, 'Grade Point', 1, 1, 'L')

        # Set font for table content
        pdf.set_font('helvetica', '', 8)

        # Example data
        data = [
            ['CS101', 'Introduction to Computer Science', 'English', '6', 'A', '4.0'],
            ['MAT201', 'Calculus I', 'English', '7', 'B+', '3.5'],
            ['EE301', 'Digital Electronics', 'English', '5', 'A-', '3.7'],
            ['PHYS101', 'Physics I', 'English', '6', 'A', '4.0'],
        ]

        # Add table content
        for row in data:
            for i in range(len(row)):
                pdf.cell(col_widths[i], 6, str(row[i]), 1)
            pdf.ln()

    def generate_pdf(self):
        # Create PDF object using FPDF
        pdf = FPDF('P', 'mm', 'Letter')

        # Set auto page break
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add a page
        pdf.add_page()

        # Call header from Info class
        Info.header(pdf)

        # Create table
        Original.create_table(pdf)

        # Call footer from Info class
        Info.footer(pdf)

        pdf.output('pdf3.pdf')


# Generate PDF using Original class
original = Original()
original.generate_pdf()
