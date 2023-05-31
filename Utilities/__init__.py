# Init Custom Selenium Module 
from    Utilities.web   import (
    Web, 
    By
)

# Init Database
from    Utilities.database  import (
    MongoClient, 
    check_database_connection
)

# Init Selenium Classes
from    Utilities.lexer import (
    OfflineParser, 
    OnlineParser,
    UserVerifier
)

# Init PDF Export module
from    Utilities.pdf_export    import (
    generate_pdf
)

# Init Utillity Functions
from    Utilities.utils import (
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

# Init Safe Run module
from    Utilities.safe_run  import (
    safe_start,
    safe_execute,
    safe_end
)