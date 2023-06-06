from abc  import ABC, abstractmethod # -> Abstraction
from fpdf import FPDF # -> Generate PDF

def calculate_perfornance(course_list : list, skip_retakens : bool = False) -> dict:
    """
    Calculates the GPA, credits attempted, credits successful and credits included in GPA based on the given course list.
    @Parameters:
        course_list - Required : The course list to calculate performance. (list) -> Used to calculate the performance of the course list.
        skip_retakens - Optional : Skip retaken courses. (bool) -> Used to skip retaken courses.
    @Returns:
        credits_attempted (int) total credits attempted.
        credits_successful (int) total credits successful.
        credits_included_in_gpa (int) total credits included in gpa.
        gpa (float) gpa.
    @Errors:
        This method should be wrapping or extracting the calculate_perfornance method in Utilities. Bu the current strcuture doesn't allow because of triangular import. In feature, this method will be turned to values.
    """
    # Initialize variables.
    credits_attempted = 0
    credits_successful = 0
    credits_included_in_gpa = 0
    gpa = 0

    # Iterate over the course list.
    for course in course_list:

        # Skip retaken courses.
        if skip_retakens:
            if course["course_code"].endswith("*"):
                continue

        # Get course variables
        course_credit : int = int(course["course_credit"])
        course_grade : str = course["course_grade"]
        course_grade_point : float = float(course["course_grade_point"])

        # Update credits attempted for each course seen
        credits_attempted += course_credit

        # Start calculating GPA
        if course_grade in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D"]:
            # If course is successful, update credits successful and credits included in GPA
            credits_successful += course_credit
            credits_included_in_gpa += course_credit
            gpa += course_grade_point
        elif course_grade in ["S"]:
            # If course is passed, update credits successful only
            credits_successful += course_credit
        elif course_grade == "F" or course_grade == "U":
            # If course is failed, update credits included in GPA
            credits_included_in_gpa += course_credit
            gpa += course_grade_point
        elif course_grade == "I":
            # If course is incomplete, do not do anything
            continue
        elif course_grade == "W":
            # If course is withdrawn, update credits attempted only
            credits_attempted -= course_credit
        elif course_grade == "N/A":
            # If course is not taken, do not do anything
            continue

    # To double check for division by zero error
    if credits_included_in_gpa == 0:
        gpa = 0
    else :
        gpa = gpa / credits_included_in_gpa
    
    # Round GPA to 2 decimal places
    gpa = round(gpa, 2)

    # Return calculated values
    return {
        "credits_attempted" : credits_attempted,
        "credits_successful" : credits_successful,
        "credits_included_in_gpa" : credits_included_in_gpa,
        "gpa" : gpa
    }

class PdfElements(ABC):
    @staticmethod
    @abstractmethod
    def write_data(pdf_buffer: FPDF, *args, **kwargs) -> None:
        """
        This method writes the data of the transcript report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            *args - Optional : Variable length argument list.
            **kwargs - Optional : Arbitrary keyword arguments.
        @Returns:
            This method does not return anything.
        """
        pass

class Header(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF, document_name : str, transcript_creation_date : str, student_school_id : str, student_name : str, student_faculty : str, language_of_instruction : str, student_national_id : str, student_surname : str, student_department : str, student_status : str, mef_logo_path : str, user_photo_path : str) -> None:
        """
        This method writes the header of the transcript report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            document_name - Required : Name of the document. (str)
            transcript_creation_date - Required : Date of the transcript creation. (str)
            student_school_id - Required : School id of the student. (str)
            student_name - Required : Name of the student. (str)
            student_faculty - Required : Faculty of the student. (str)
            language_of_instruction - Required : Language of instruction. (str)
            student_national_id - Required : National id of the student. (str)
            student_surname - Required : Surname of the student. (str)
            student_department - Required : Department of the student. (str)
            student_status - Required : Status of the student. (str)
            mef_logo_path - Required : Path to the logo of the university. (str)
            user_photo_path - Required : Path to the photo of the student. (str)
        @Returns:
            This method does not return anything.
        """
        # Set a sizes for header photos.
        photo_sizes = (35, 30)

        # Logo.
        pdf_buffer.image(mef_logo_path, 10, 8, *photo_sizes)
        # User photo.
        pdf_buffer.image(user_photo_path, 165, 8, *photo_sizes)

        # Put offset title and page.
        pdf_buffer.ln(3)

        # Title.
        title = document_name
        # Font for title.
        pdf_buffer.set_font("helvetica", "B", 21)
        # Calculate width of the title and position.
        title_w = pdf_buffer.get_string_width(title) + 6
        doc_w = pdf_buffer.w
        pdf_buffer.set_x((doc_w - title_w) / 2)
        # Title.
        pdf_buffer.cell(title_w, 10, title, border=False, ln=1, align="C")

        # Put space between title and date.
        pdf_buffer.ln(2)

        # Date.
        date = transcript_creation_date
        # Font for date.
        pdf_buffer.set_font("helvetica", "B", 15)
        # Calculate width of the date and position.
        date_w = pdf_buffer.get_string_width(date) + 6
        doc_w = pdf_buffer.w
        pdf_buffer.set_x((doc_w - date_w) / 2)
        # Date.
        pdf_buffer.cell(date_w, 10, date, border=False, ln=1, align="C")

        # Line break.
        pdf_buffer.ln(14)

        # Set a translation map encoding handling Turkish characters.
        transmap = str.maketrans("ığĞüÜşŞİöÖçÇ", "igGuUsSIoOcC")
        
        # Student Information Table, applied translation map to all values.
        student_info_labels = ["Student ID", "Name", "Faculty/Department", "Language of Instruction"]
        student_info_values = [student_school_id.translate(transmap), student_name.translate(transmap), student_faculty.split("/")[0].strip().translate(transmap), language_of_instruction.translate(transmap)]
        additional_info_labels = ["National ID", "Surname", "Program Name", "Student Status"]
        additional_info_values = [student_national_id.translate(transmap), student_surname.translate(transmap), student_department.translate(transmap), student_status.translate(transmap)]

        # Set column widths.
        col_widths = [32, 85, 28, 45]

        # Iterate over (student information labels and values) times, and put them up.
        for i in range(4) :
            # Set font for labels and values.
            pdf_buffer.set_font("helvetica", "", 8)
            pdf_buffer.cell(col_widths[0], 7, student_info_labels[i], 1, 0, "L")
            pdf_buffer.set_font("helvetica", "B", 8)
            pdf_buffer.cell(col_widths[1], 7, student_info_values[i], 1, 0, "L")
            pdf_buffer.set_font("helvetica", "", 8)
            pdf_buffer.cell(col_widths[2], 7, additional_info_labels[i], 1, 0, "L")
            pdf_buffer.set_font("helvetica", "B", 8)
            pdf_buffer.cell(col_widths[3], 7, additional_info_values[i], 1, 1, "L")

class OriginalCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF, semesters: dict) -> None:
        """
        This method writes the original courses part of the transcript report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            semesters - Required : The semester data. (dict)
        @Returns:
            This method does not return anything.
        """
        # Give a title to the table for displaying.
        table_title = "Original Transcript"
        # Calculate width of the table title.
        original_transcript_title_w = pdf_buffer.get_string_width(table_title) + 6
        # Calculate the position to align it with the "Transcript Document" title.
        original_transcript_x = (pdf_buffer.w - original_transcript_title_w) / 2

        # Set font and position for table title.
        pdf_buffer.set_font("helvetica", "B", 13)
        pdf_buffer.set_x(original_transcript_x)
        pdf_buffer.cell(original_transcript_title_w, 10, table_title, ln=2, align="C")

        # Reset font settings for the table.
        pdf_buffer.set_font("helvetica", "B", 8)
        # Add extra spacing after the title.
        pdf_buffer.ln(5)

        # Set column widths.
        col_widths = [25, 85, 25, 15, 15, 25]
        col_widths_extrarow = [25, 42.5, 42.5, 55, 25]
        # Set fill color for header row.
        pdf_buffer.set_fill_color(255, 255, 255)
        # Set font size to 8 for other headers.
        pdf_buffer.set_font("helvetica", "B", 8)
        
        # Expand all courses into one to calculate general GPA later.
        all_courses = []

        # Iterate over semesters.
        for semester_key, semester_data in semesters.items() :
            # Get the courses.
            semester_definition = semester_data["semester_definition"]
            course_list = semester_data["course_list"]

            # Expand all courses into one to calculate general GPA later.
            all_courses.extend(course_list)
            
            # Add new merged row for semester.
            total_width = sum(col_widths)
            pdf_buffer.set_font("helvetica", "B", 10)
            # Set fill color for new row.
            pdf_buffer.set_fill_color(192, 192, 192)
            # Merge cells.
            pdf_buffer.cell(total_width, 6, semester_definition, 1, 1, "C", 1)
            
            # Add table header.
            pdf_buffer.cell(col_widths[0], 6, "Course Code", 1, 0, "C")
            pdf_buffer.cell(col_widths[1], 6, "Course Name", 1, 0, "C")
            pdf_buffer.cell(col_widths[2], 6, "Language", 1, 0, "C")
            pdf_buffer.cell(col_widths[3], 6, "ECTS", 1, 0, "C")
            pdf_buffer.cell(col_widths[4], 6, "Grade", 1, 0, "C")
            pdf_buffer.cell(col_widths[5], 6, "Grade Point", 1, 1, "C")

            # Set font for table content.
            pdf_buffer.set_font("helvetica", "", 8)

            # Add table content.
            for course in course_list:
                try :
                    # Add cells row for course.
                    pdf_buffer.cell(col_widths[0], 6, course["course_code"], 1, 0, "C")
                    pdf_buffer.cell(col_widths[1], 6, course["course_name"], 1, 0, "C")
                    pdf_buffer.cell(col_widths[2], 6, course["course_lang"], 1, 0, "C")
                    pdf_buffer.cell(col_widths[3], 6, course["course_credit"], 1, 0, "C")
                    pdf_buffer.cell(col_widths[4], 6, course["course_grade"], 1, 0, "C")
                    pdf_buffer.cell(col_widths[5], 6, course["course_grade_point"], 1, 1, "C")
                except UnicodeEncodeError :
                    print("UnicodeEncodeError Warning for PDF Extraction -> Please check your semester course list, there is a course with a non-english character in it.")
                    pass

            # Calculate performance for the semester.
            performance = calculate_perfornance(course_list, skip_retakens=True)

            # Add extra row for semester details.
            pdf_buffer.set_fill_color(135, 206, 250)
            pdf_buffer.set_font("helvetica", "b", 8)
            pdf_buffer.set_fill_color(255, 255, 255)
            
            # Add spacing after the semester.
            pdf_buffer.ln(2)
            # Semester label.
            pdf_buffer.cell(col_widths_extrarow[0], 6, "Semester", 1, 0, "C")
            # Attempted Credits label.
            pdf_buffer.cell(col_widths_extrarow[1], 6, "Attempted Credits: " + str(performance["credits_attempted"]), 1, 0, "C")
            # Successful Credits label.
            pdf_buffer.cell(col_widths_extrarow[2], 6, "Successful Credits: " + str(performance["credits_successful"]), 1, 0, "C")
            # Credits Included in GPA label.
            pdf_buffer.cell(col_widths_extrarow[3], 6, "Credits Included in GPA: " + str(performance["credits_included_in_gpa"]), 1, 0, "C")
            # GPA label.
            pdf_buffer.cell(col_widths_extrarow[4], 6, "GPA: " + str(performance["gpa"]), 1, 1, "C")
            
            # If semester_key not the last semester, then add new line.
            if semester_key != list(semesters.keys())[-1]:
                # Seperate tables.
                pdf_buffer.ln(5)
            else :
                # If last semester, then seperate more.
                pdf_buffer.ln(10)
            
        # Calculate performance for the semester.
        performance = calculate_perfornance(all_courses, skip_retakens=True)

        # Set font for extra row.
        pdf_buffer.set_font("helvetica", "b", 9)
        
        #Add extra row for semester details.
        # Semester label.
        pdf_buffer.cell(col_widths_extrarow[0], 6, "General", 1, 0, "C")
        # Attempted Credits label.
        pdf_buffer.cell(col_widths_extrarow[1], 6, "Attempted Credits: " + str(performance["credits_attempted"]), 1, 0, "C")
        # Successful Credits label.
        pdf_buffer.cell(col_widths_extrarow[2], 6, "Successful Credits: " + str(performance["credits_successful"]), 1, 0, "C")
        # Credits Included in GPA label.
        pdf_buffer.cell(col_widths_extrarow[3], 6, "Credits Included in GPA: " + str(performance["credits_included_in_gpa"]), 1, 0, "C")
        # GPA label.
        pdf_buffer.cell(col_widths_extrarow[4], 6, "GPA: " + str(performance["gpa"]), 1, 1, "C")

class ModifiedCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF, modified_course_list: list) -> None:
        """
        This method writes the modified courses part of the transcript report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            semesters - modified_course_list : The course data. (list)
        @Returns:
            This method does not return anything.
        """
        # Give a title to the table for displaying.
        table_title = "Modified Transcript"
        # Calculate width of the table title.
        original_transcript_title_w = pdf_buffer.get_string_width(table_title) + 6
        # Calculate the position to align it with the "Transcript Document" title.
        original_transcript_x = (pdf_buffer.w - original_transcript_title_w) / 2

        # Set font and position for table title.
        pdf_buffer.set_font("helvetica", "B", 13)
        pdf_buffer.set_x(original_transcript_x)
        pdf_buffer.cell(original_transcript_title_w, 10, table_title, ln=2, align="C")

        # Reset font settings for the table.
        pdf_buffer.set_font("helvetica", "B", 8)
        # Add extra spacing after the title.
        pdf_buffer.ln(5)

        # Set column widths.
        col_widths = [25, 85, 25, 15, 15, 25]
        col_widths_extrarow = [25, 42.5, 42.5, 55, 25]

        # Set font size to 8 for other headers.
        pdf_buffer.set_font("helvetica", "B", 8)
        # Set fill color for new row.
        pdf_buffer.set_fill_color(192, 192, 192)
  
        # Add new merged row for semester.
        total_width = sum(col_widths)
        # Set font for new row.
        pdf_buffer.set_font("helvetica", "B", 10)
        # Set fill color for new row.
        pdf_buffer.set_fill_color(192, 192, 192)
        # Merge cells for the new row.
        pdf_buffer.cell(total_width, 6, table_title, 1, 1, "C", 1)

        # Add table header.
        pdf_buffer.cell(col_widths[0], 6, "Course Code", 1, 0, "C")
        pdf_buffer.cell(col_widths[1], 6, "Course Name", 1, 0, "C")
        pdf_buffer.cell(col_widths[2], 6, "Language", 1, 0, "C")
        pdf_buffer.cell(col_widths[3], 6, "ECTS", 1, 0, "C")
        pdf_buffer.cell(col_widths[4], 6, "Grade", 1, 0, "C")
        pdf_buffer.cell(col_widths[5], 6, "Grade Point", 1, 1, "C")
        
        # Set font for table content.
        pdf_buffer.set_font("helvetica", "", 8)

        # Add table content.
        for course in modified_course_list:
            # Set fill color for content rows.
            pdf_buffer.set_fill_color(255, 100, 100)
            try :
                # Add cells row for course.
                pdf_buffer.cell(col_widths[0], 6, str(course["course_code"]), 1, 0, "C")
                pdf_buffer.cell(col_widths[1], 6, str(course["course_name"]), 1, 0, "C")
                pdf_buffer.cell(col_widths[2], 6, str(course["course_lang"]), 1, 0, "C")
                pdf_buffer.cell(col_widths[3], 6, str(course["course_credit"]), 1, 0, "C")
                pdf_buffer.cell(col_widths[4], 6, str(course["course_grade"]), 1, 0, "C")
                pdf_buffer.cell(col_widths[5], 6, str(course["course_grade_point"]), 1, 1, "C")
            except UnicodeEncodeError :
                print("UnicodeEncodeError Warning for PDF Extraction -> Please check your modified course list, there is a course with a non-english character in it.")
                pass

        # Calculate performance for the semester.
        performance = calculate_perfornance(modified_course_list, skip_retakens=True)

        # Add extra row for semester details.
        pdf_buffer.set_fill_color(255, 100, 100)
        pdf_buffer.set_font("helvetica", "b", 8)
        
        # Add spacing after the semester.
        pdf_buffer.ln(2)
        # Set fill color for extra row.
        pdf_buffer.set_fill_color(255, 100, 100)
        # Semester label.
        pdf_buffer.cell(col_widths_extrarow[0], 6, "General", 1, 0, "C")
        # Attempted Credits label.
        pdf_buffer.cell(col_widths_extrarow[1], 6, "Attempted Credits: " + str(performance["credits_attempted"]), 1, 0, "C")
        # Successful Credits label.
        pdf_buffer.cell(col_widths_extrarow[2], 6, "Successful Credits: " + str(performance["credits_successful"]), 1, 0, "C")
        # Credits Included in GPA label.
        pdf_buffer.cell(col_widths_extrarow[3], 6, "Credits Included in GPA: " + str(performance["credits_included_in_gpa"]), 1, 0, "C")
        # GPA label.
        pdf_buffer.cell(col_widths_extrarow[4], 6, "GPA: " + str(performance["gpa"]), 1, 1, "C")

class Modifications(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF, filtering : list, sorting : dict, updated_course_list : list, subtracted_course_list : list, added_course_list : list, original_course_list: list) -> None:
        """
        This method writes the changes | done modifications in the transcript manager of the Transcript Report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            filtering - Required : The filtering options. (list)
            sorting - Required : The sorting options. (dict)
            updated_course_list - Required : The updated course list. (list)
            subtracted_course_list - Required : The subtracted course list. (list)
            added_course_list - Required : The added course list. (list)
            original_course_list - Required : The original course list. (list)
        @Returns:
            This method does not return anything.
        """
        # Give a title to the table for displaying.
        table_title = "Modifications"
        # Calculate width of the table title.
        original_transcript_title_w = pdf_buffer.get_string_width(table_title) + 6
        # Calculate the position to align it with the "Transcript Document" title.
        original_transcript_x = (pdf_buffer.w - original_transcript_title_w) / 2

        # Set font and position for table title.
        pdf_buffer.set_font("helvetica", "B", 13)
        pdf_buffer.set_x(original_transcript_x)
        pdf_buffer.cell(original_transcript_title_w, 10, table_title, ln=2, align="C")

        # Add extra spacing after the title.
        pdf_buffer.ln(5)

        # Set a spacing factor between the info.
        info_space = 5

        # Write applied filters.
        Filterings.write_data(pdf_buffer, filtering)
        # Add extra spacing after the info.
        pdf_buffer.ln(info_space)

        # Write applied sorting.
        Sorting.write_data(pdf_buffer, sorting)
        # Add extra spacing after the info.
        pdf_buffer.ln(info_space)

        # Write updated courses.
        UpdatedCourses.write_data(pdf_buffer, updated_course_list, original_course_list)
        # Add extra spacing after the info.
        pdf_buffer.ln(info_space)

        # Write added courses.
        AddedCourses.write_data(pdf_buffer, added_course_list)
        # Add extra spacing after the info.
        pdf_buffer.ln(info_space)

        # Write removed courses.
        RemovedCourses.write_data(pdf_buffer, subtracted_course_list)

class Filterings(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF, filtering : list) -> None:
        """
        This method writes filterings of the Transcript Report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            filtering - Required : The filtering options. (list)
        @Returns:
            This method does not return anything.
        """
        # Set a table title.
        table_title = "Applied Filtering"

        # Reset font settings for the table
        pdf_buffer.set_font("helvetica", "B", 8)

        # Set column widths
        col_widths = [95, 95]

        # Add new merged row for semester.
        total_width = sum(col_widths)
        # Set font for new row.
        pdf_buffer.set_font("helvetica", "B", 10)
        # Set fill color for new row.
        pdf_buffer.set_fill_color(192, 192, 192)
        # Merge cells for the new row.
        pdf_buffer.cell(total_width, 6, table_title, 1, 1, "C", 1)

        # Set font size to 8 for other headers
        pdf_buffer.set_font("helvetica", "B", 8)
        # Set fill color for new row
        pdf_buffer.set_fill_color(192, 192, 192)
  
        # Add table header
        pdf_buffer.cell(col_widths[0], 6, "Filtered By", 1, 0, "C")
        pdf_buffer.cell(col_widths[1], 6, "Filtered With", 1, 1, "C")

        # Set font for table content
        pdf_buffer.set_font("helvetica", "", 8)

        display_map = {"course_code" : "Course Code", "course_name" : "Course Name", "course_lang" : "Course Language", "course_credit" : "Course Credit", "course_grade" : "Course Grade", "course_grade_point" : "Course Grade Point"}

        if len(filtering) != 0:
            # Add table content | Set fill color for content rows.
            for filter in filtering:
                pdf_buffer.set_fill_color(255, 100, 100)
                try:
                    # Add table content.
                    pdf_buffer.cell(col_widths[0], 6, str(display_map[filter["filter_key"]]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[1], 6, str(filter["filter_value"]), 1, 1, "C")
                except UnicodeEncodeError :
                    print("UnicodeEncodeError Warning for PDF Extraction -> Please check your filterings, there is a course with a non-english character in it.")
                    pass
        else :
            # Put an info message when there is no info.
            pdf_buffer.cell(total_width, 6, "No Filter Exist", 1, 1, "C")

class Sorting(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF, sorting : dict) -> None:
        """
        This method writes sortings of the Transcript Report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            sorting - Required : The last sorting done. (dict)
        @Returns:
            This method does not return anything.
        """
        # Set a table title.
        table_title = "Applied Sorting"

        # Reset font settings for the table
        pdf_buffer.set_font("helvetica", "B", 8)

        # Set column widths
        col_widths = [95, 95]

        # Add new merged row for semester.
        total_width = sum(col_widths)
        # Set font for new row.
        pdf_buffer.set_font("helvetica", "B", 10)
        # Set fill color for new row.
        pdf_buffer.set_fill_color(192, 192, 192)
        # Merge cells for the new row.
        pdf_buffer.cell(total_width, 6, table_title, 1, 1, "C", 1)

        # Set font size to 8 for other headers
        pdf_buffer.set_font("helvetica", "B", 8)
        # Set fill color for new row
        pdf_buffer.set_fill_color(192, 192, 192)
  
        # Add table header
        pdf_buffer.cell(col_widths[0], 6, "Sorted By", 1, 0, "C")
        pdf_buffer.cell(col_widths[1], 6, "Sorted With", 1, 1, "C")

        # Set font for table content
        pdf_buffer.set_font("helvetica", "", 8)

        display_map = {"course_code" : "Course Code", "course_name" : "Course Name", "course_lang" : "Course Language", "course_credit" : "Course Credit", "course_grade" : "Course Grade", "course_grade_point" : "Course Grade Point"}

        if not (sorting["sort_key"] is None or sorting["should_reverse"] is None):
            # Add table content | Set fill color for content rows.
            pdf_buffer.set_fill_color(255, 100, 100)
            try:
                # Add table content.
                pdf_buffer.cell(col_widths[0], 6, str(display_map[sorting["sort_key"]]), 1, 0, "C")
                pdf_buffer.cell(col_widths[1], 6, "Ascending Order" if sorting["should_reverse"] else "Descending Order", 1, 1, "C")
            except UnicodeEncodeError :
                print("UnicodeEncodeError Warning for PDF Extraction -> Please check your filterings, there is a course with a non-english character in it.")
                pass
        else :
            # Put an info message when there is no info.
            pdf_buffer.cell(total_width, 6, "No Sort Exist", 1, 1, "C")

class UpdatedCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF, updated_course_list: list, original_course_list: list) -> None:
        """
        This method writes the changes | done modifications in the transcript manager of the Transcript Report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            updated_course_list - Required : The updated course list. (list)
            original_course_list - Required : The original course list. (list)
        @Returns:
            This method does not return anything.
        """
        # Set a table title.
        table_title = "Updated Courses"

        # Reset font settings for the table.
        pdf_buffer.set_font("helvetica", "B", 8)

        # Set column widths.
        col_widths = [25, 60, 25, 15, 20, 20, 25]

        # Add new merged row for semester.
        total_width = sum(col_widths)
        # Set font for new row.
        pdf_buffer.set_font("helvetica", "B", 10)
        # Set fill color for new row.
        pdf_buffer.set_fill_color(192, 192, 192)
        # Merge cells for the new row.
        pdf_buffer.cell(total_width, 6, table_title, 1, 1, "C", 1)

        # Set font size to 8 for other headers.
        pdf_buffer.set_font("helvetica", "B", 8)
        # Set fill color for new row.
        pdf_buffer.set_fill_color(192, 192, 192)
  
        # Add table header.
        pdf_buffer.cell(col_widths[0], 6, "Course Code", 1, 0, "C")
        pdf_buffer.cell(col_widths[1], 6, "Course Name", 1, 0, "C")
        pdf_buffer.cell(col_widths[2], 6, "Language", 1, 0, "C")
        pdf_buffer.cell(col_widths[3], 6, "ECTS", 1, 0, "C")
        pdf_buffer.cell(col_widths[4], 6, "Old Grade", 1, 0, "C")
        pdf_buffer.cell(col_widths[5], 6, "New Grade", 1, 0, "C")
        pdf_buffer.cell(col_widths[6], 6, "Grade Point", 1, 1, "C")
        
        # Set font for table content.
        pdf_buffer.set_font("helvetica", "", 8)

        # Get default course codes.
        default_course_codes = [course["course_code"] for course in original_course_list]
        # Catch changed grades.
        for course in updated_course_list:
            course_code = course["course_code"]
            # Check if exist.
            if course_code in default_course_codes :
                index = default_course_codes.index(course_code)
                default_course = original_course_list[index]
                # Then get previous grade.
                previous_grade = default_course["course_grade"]
            else :
                # Else put empty string.
                previous_grade = ""

            # Add previous grade to the course.
            course["previous_course_grade"] = previous_grade

        if len(updated_course_list) != 0:
            # Add table content.
            for course in updated_course_list:
                # Set fill color for content rows.
                pdf_buffer.set_fill_color(255, 100, 100)
                try:
                    # Add table content.
                    pdf_buffer.cell(col_widths[0], 6, str(course["course_code"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[1], 6, str(course["course_name"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[2], 6, str(course["course_lang"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[3], 6, str(course["course_credit"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[4], 6, str(course["previous_course_grade"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[5], 6, str(course["course_grade"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[6], 6, str(course["course_grade_point"]), 1, 1, "C")
                except UnicodeEncodeError :
                    print("UnicodeEncodeError Warning for PDF Extraction -> Please check your updated course list, there is a course with a non-english character in it.")
                    pass
        else:
            # Put an info message when there is no info.
            pdf_buffer.cell(total_width, 6, "No Updated Course Exist", 1, 1, "C")

class AddedCourses(PdfElements, FPDF):
     @staticmethod
     def write_data(pdf_buffer: FPDF, added_course_list: list) -> None:
        """
        This method writes the changes | done modifications in the transcript manager of the Transcript Report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            added_course_list - Required : The added course list. (list)
        @Returns:
            This method does not return anything.
        """
        # Set a table title.
        table_title = "Added Courses"

        # Reset font settings for the table
        pdf_buffer.set_font("helvetica", "B", 8)

        # Set column widths
        col_widths = [25, 85, 25, 15, 15, 25]

        # Add new merged row for semester.
        total_width = sum(col_widths)
        # Set font for new row.
        pdf_buffer.set_font("helvetica", "B", 10)
        # Set fill color for new row.
        pdf_buffer.set_fill_color(192, 192, 192)
        # Merge cells for the new row.
        pdf_buffer.cell(total_width, 6, table_title, 1, 1, "C", 1)

        # Set font size to 8 for other headers
        pdf_buffer.set_font("helvetica", "B", 8)
        # Set fill color for new row
        pdf_buffer.set_fill_color(192, 192, 192)
  
        # Add table header
        pdf_buffer.cell(col_widths[0], 6, "Course Code", 1, 0, "C")
        pdf_buffer.cell(col_widths[1], 6, "Course Name", 1, 0, "C")
        pdf_buffer.cell(col_widths[2], 6, "Language", 1, 0, "C")
        pdf_buffer.cell(col_widths[3], 6, "ECTS", 1, 0, "C")
        pdf_buffer.cell(col_widths[4], 6, "Grade", 1, 0, "C")
        pdf_buffer.cell(col_widths[5], 6, "Grade Point", 1, 1, "C")

        # Set font for table content
        pdf_buffer.set_font("helvetica", "", 8)

        if len(added_course_list) != 0:
            # Add table content
            for course in added_course_list:
                # Set fill color for content rows.
                pdf_buffer.set_fill_color(255, 100, 100)
                try:
                    # Add table content.
                    pdf_buffer.cell(col_widths[0], 6, str(course["course_code"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[1], 6, str(course["course_name"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[2], 6, str(course["course_lang"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[3], 6, str(course["course_credit"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[4], 6, str(course["course_grade"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[5], 6, str(course["course_grade_point"]), 1, 1, "C")
                except UnicodeEncodeError :
                    print("UnicodeEncodeError Warning for PDF Extraction -> Please check your added course list, there is a course with a non-english character in it.")
                    pass
        else :
            # Put an info message when there is no info.
            pdf_buffer.cell(total_width, 6, "No Added Course Exist", 1, 1, "C")

class RemovedCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF, subtracted_course_list: list) -> None:
        """
        This method writes the changes | done modifications in the transcript manager of the Transcript Report.
        @Parameters:
            pdf_buffer - Required : The buffer of the pdf file. (FPDF)
            subtracted_course_list - Required : The removed course list. (list)
        @Returns:
            This method does not return anything.
        """
        # Set a table title.
        table_title = "Removed Courses"

        # Reset font settings for the table
        pdf_buffer.set_font("helvetica", "B", 8)

        # Set column widths
        col_widths = [25, 85, 25, 15, 15, 25]

        # Add new merged row for semester.
        total_width = sum(col_widths)
        # Set font for new row.
        pdf_buffer.set_font("helvetica", "B", 10)
        # Set fill color for new row.
        pdf_buffer.set_fill_color(192, 192, 192)
        # Merge cells for the new row.
        pdf_buffer.cell(total_width, 6, table_title, 1, 1, "C", 1)

        # Set font size to 8 for other headers
        pdf_buffer.set_font("helvetica", "B", 8)
        # Set fill color for new row
        pdf_buffer.set_fill_color(192, 192, 192)
  
        # Add table header
        pdf_buffer.cell(col_widths[0], 6, "Course Code", 1, 0, "C")
        pdf_buffer.cell(col_widths[1], 6, "Course Name", 1, 0, "C")
        pdf_buffer.cell(col_widths[2], 6, "Language", 1, 0, "C")
        pdf_buffer.cell(col_widths[3], 6, "ECTS", 1, 0, "C")
        pdf_buffer.cell(col_widths[4], 6, "Grade", 1, 0, "C")
        pdf_buffer.cell(col_widths[5], 6, "Grade Point", 1, 1, "C")

        # Set font for table content
        pdf_buffer.set_font("helvetica", "", 8)

        if len(subtracted_course_list) != 0:
            # Add table content
            for course in subtracted_course_list:
                # Set fill color for content rows.
                pdf_buffer.set_fill_color(255, 100, 100)
                try:
                    # Add table content.
                    pdf_buffer.cell(col_widths[0], 6, str(course["course_code"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[1], 6, str(course["course_name"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[2], 6, str(course["course_lang"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[3], 6, str(course["course_credit"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[4], 6, str(course["course_grade"]), 1, 0, "C")
                    pdf_buffer.cell(col_widths[5], 6, str(course["course_grade_point"]), 1, 1, "C")
                except UnicodeEncodeError :
                    print("UnicodeEncodeError Warning for PDF Extraction -> Please check your removed course list, there is a course with a non-english character in it.")
                    pass
        else :
            # Put an info message when there is no info.
            pdf_buffer.cell(total_width, 6, "No Removed Course Exist", 1, 1, "C")

class TranscriptReport(FPDF):

    def __init__(self, orientation = "portrait", unit = "mm", format = "A4") -> None:
        """
        This method initializes the Transcript Report.
        @Parameters:
            orientation - Optional : The orientation of the pdf file. (str)
            unit - Optional : The unit of the pdf file. (str)
            format - Optional : The format of the pdf file. (str)
        @Returns:
            This method does not return anything.
        """
        # Initialize the parent class.
        super().__init__(orientation, unit, format)

        # Set margins.
        self.set_margins(10, 10, 10)

        # Add a new page.
        self.move()

        # Set auto page break.
        self.set_auto_page_break(auto=True, margin=15)

        # Set manuals.
        self.set_keywords("transcript, report, pdf, python, fpdf")
        self.set_creator("FPDF")
        self.set_author("Trancript Manager")
        self.set_title("Transcript Report")

    def seperate(self, nl_amount : int = 1) -> None:
        """
        This method seperates the pdf file.
        @Parameters:
            nl_amount - Optional : The amount of new lines. (int) (default : 1)
        @Returns:
            This method does not return anything.
        """
        # Add new lines.
        self.ln(nl_amount)

    def move(self) -> None:
        """
        This method moves the pdf file.
        @Parameters:
            This method does not take any parameters.
        @Returns:
            This method does not return anything.
        """
        # Add a new page.
        self.add_page()

def generate_pdf(user_info_document : dict, user_data_document : dict, user_photo_path : str, mef_logo_path : str, output_file_path : str) -> None:
    """
    This function generates the PDF file of the transcript.
    @Parameters:
        user_info_document - Required : The user info document. (dict) -> Used to get the user info.
        user_data_document - Required : The user data document. (dict) -> Used to get the user data.
        user_photo_path - Required : The path of the user photo. (str) -> Used to get the user photo.
        mef_logo_path - Required : The path of the mef logo. (str) -> Used to get the mef logo.
        output_file_path - Required : The path of the output file. (str) -> Used to save the PDF file.
    @Returns:
        None
    @@Contributors:
        @tuana_selen_ozhazday
    """
    # get the user info literals
    language_of_instruction = user_info_document["language_of_instruction"]
    student_department = user_info_document["student_department"]
    student_faculty = user_info_document["student_faculty"]
    student_name = user_info_document["student_name"]
    student_school_id = user_info_document["student_school_id"]
    student_national_id = user_info_document["_id"]
    student_status = user_info_document["student_status"]
    student_surname = user_info_document["student_surname"]

    # get the user data literals
    transcript_creation_date = user_data_document["transcript_creation_date"]
    semesters = user_data_document["semesters"]
    original_course_list = user_data_document["original_course_list"]
    filtering = user_data_document["filtering"]
    sorting = user_data_document["sorting"]
    modified_course_list = user_data_document["modified_course_list"]
    document_name = user_data_document["document_name"]
    updated_course_list = user_data_document["updated_course_list"]
    subtracted_course_list = user_data_document["subtracted_course_list"]
    added_course_list = user_data_document["added_course_list"]
    
    # Create the pdf buffer.
    pdf = TranscriptReport()
    
    # Write header into the buffer.
    Header.write_data(pdf, document_name, transcript_creation_date, student_school_id, student_name, student_faculty, language_of_instruction, student_national_id, student_surname, student_department, student_status, mef_logo_path, user_photo_path)
    # Add a seperator.
    pdf.seperate(7)
    
    # Write the body into the buffer.
    OriginalCourses.write_data(pdf, semesters)
    # Add a new page.
    pdf.move()
    
    # Write the body into the buffer.
    Modifications.write_data(pdf, filtering, sorting, updated_course_list, subtracted_course_list, added_course_list, original_course_list)
    # Add a new page.
    pdf.move()
    
    # Write the body into the buffer.
    ModifiedCourses.write_data(pdf, modified_course_list)

    # Save the pdf file.
    pdf.output(output_file_path)