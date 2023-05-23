from    DIRECT_EXECUTION import sort_by, filter_by, add_course, subtract_course, update_course, calculate_performance
from    DIRECT_EXECUTION import translate
from    abc     import  ABC, abstractmethod
from    fpdf    import  FPDF
import  json

class PdfElements(ABC):
    @staticmethod
    @abstractmethod
    def write_data(pdf_buffer: FPDF, *args, **kwargs) -> None:
        pass

class Header(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class Student(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class Semesters(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class OriginalCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class AddedCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class RemovedCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class AppliedOperations(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class UpdatedCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class ModifiedCourses(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class Footer(PdfElements, FPDF):
    @staticmethod
    def write_data(pdf_buffer: FPDF) -> None:
        pass

class TranscriptReport(FPDF):

    def __init__(self, orientation = "portrait", unit = "mm", format = "A4") -> None:
        super().__init__(orientation, unit, format)

        self.set_margins(10, 10, 10)

        self.add_page()

        self.set_auto_page_break(auto=True, margin=15)

        self.set_keywords("transcript, report, pdf, python, fpdf")
        self.set_creator("FPDF")
        self.set_author("Trancript Manager")
        self.set_title("Transcript Report")

if __name__ == "__main__":
############################################################FUNCTION PARAMETERS
    with open(r"DIRECT_EXECUTION\user_data_out.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)
    with open(r"DIRECT_EXECUTION\user_info_out.json", "r", encoding="utf-8") as f:
        user_info = json.load(f)

    user_info_document = user_info
    user_data_document = user_data
    user_photo_path = r"DIRECT_EXECUTION\user_.png"
    output_file_path = user_data["document_name"] + ".pdf"
#######################################################################LITERALS
    language_of_instruction = user_info_document["language_of_instruction"]
    student_department = user_info_document["student_department"]
    student_faculty = user_info_document["student_faculty"]
    student_name = user_info_document["student_name"]
    student_school_id = user_info_document["student_school_id"]
    student_national_id = user_info_document["_id"]
    student_status = user_info_document["student_status"]
    student_surname = user_info_document["student_surname"]

    owner_id = user_data_document["owner_id"]
    parsing_type = user_data_document["parsing_type"]
    parsing_language = user_data_document["parsing_language"]
    transcript_manager_date = user_data_document["transcript_manager_date"]
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
###################################################################DRIVER_CODE
    pdf = TranscriptReport()

    Header.write_data(pdf)
    Student.write_data(pdf)
    Semesters.write_data(pdf)
    OriginalCourses.write_data(pdf)
    AddedCourses.write_data(pdf)
    RemovedCourses.write_data(pdf)
    AppliedOperations.write_data(pdf)
    UpdatedCourses.write_data(pdf)
    ModifiedCourses.write_data(pdf)
    Footer.write_data(pdf)

    pdf.output("test.pdf")

