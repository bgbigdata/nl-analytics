scalaVersion := "2.10.6"
scalacOptions ++= Seq("-deprecation", "-feature", "-unchecked", "-Xlint")
scalacOptions ++= Seq("-encoding", "UTF-8")
javacOptions ++= Seq("-encoding", "UTF-8")
resolvers += "Atilika Open Source repository" at "http://www.atilika.org/nexus/content/repositories/atilika"
libraryDependencies ++= Seq(
	"org.scalaj" %% "scalaj-http" % "2.3.0",
	"org.atilika.kuromoji" % "kuromoji" % "0.7.7",
	"org.deeplearning4j" % "deeplearning4j-core" % "0.8.0",
	"org.deeplearning4j" % "deeplearning4j-nlp" % "0.8.0",
	"org.nd4j" % "nd4j-native" % "0.8.0" classifier "" classifier "windows-x86_64",
	"org.slf4j" % "slf4j-api" % "1.7.25",
	"org.apache.logging.log4j" % "log4j-core" % "2.8.2",
	"ch.qos.logback" % "logback-classic" % "1.2.3"
)