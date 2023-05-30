from Utilities.web import (
    Web, 
    By
)

from Utilities.database import (
    MongoClient, 
    check_database_connection
)

from Utilities.lexer import (
    OfflineParser, 
    OnlineParser,
    UserVerifier
)

from Utilities.pdf_export import (
    generate_pdf
)

from Utilities.utils import (
    get_gif_frame_count,
    authenticate,
    validate_transcript,
    check_internet_connection,
    get_connection_details,
    download_chrome_driver,
    push_dpi,
    get_gender,
    translate_text,
    
    sort_by,
    filter_by,
    add_course,
    subtract_course,
    update_course,
    calculate_performance,

    generate_gradient_colors

)

from Utilities.safe_run import (
    safe_start,
    safe_execute,
    safe_end
)