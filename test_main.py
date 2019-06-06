import message_mngr
import server_connect
import fetch_rfc822

connection = server_connect.open_connection()
message_mngr.search_all(connection)
fetch_rfc822.fetch_message("INBOX", "10", connection)
connection.logout()
exit(0)
