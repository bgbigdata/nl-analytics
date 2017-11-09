package Hello

import java.sql.{DriverManager, Connection, Statement, ResultSet, SQLException}

object SqlSelect {
  def main(args : Array[String]) : Unit = {
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
          }
          stmt.close()
      } catch {
         case e:SQLException => println("Database error "+e)

         case e => {
           println("Some other exception type:")
           e.printStackTrace()
         }
      } finally {
         con.close()
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