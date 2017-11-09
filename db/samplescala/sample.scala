package Hello

import java.sql.{DriverManager, Connection, Statement, ResultSet, SQLException}
import java.io.PrintWriter

object SqlSelect {
  def main(args : Array[String]) : Unit = {
	val out1 = new PrintWriter("out.txt")
    try {
        Class.forName("com.mysql.jdbc.Driver").newInstance();
        var con = 
            DriverManager.getConnection("jdbc:mysql://localhost/nl_analytics?" + 
                                   "user=dbuser1&password=P@ssw0rd");
        try {
           var stmt = con.createStatement()
           var rs = stmt.executeQuery("SELECT * FROM rawtext")
           while (rs.next()){
              print(rs.getString(1) + " ")
              print(rs.getString(2) + " ")
              print(rs.getString(3) + " ")
              println(rs.getString(4))
			out1.write(rs.getString(1) + " ")
			out1.write(rs.getString(2) + " ")
			out1.write(rs.getString(3) + " ")
			out1.write(rs.getString(4) + "\r\n")
          }          
//           var rs = stmt.executeUpdate("INSERT INTO rawtext VALUES('0x11112','twitter','1','日本語ニュース')")
          stmt.close()
      } catch {
         case e:SQLException => println("Database error "+e)

         case e => {
           println("Some other exception type:")
           e.printStackTrace()
         }
      } finally {
         con.close()
         out1.close()
      }
   } catch {
      case e:SQLException => println("Database error "+e)
      case e => {
        println("Some other exception type:")
        e.printStackTrace()
     }
  }
 }
}