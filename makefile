JFLAGS = -g
JC = javac
.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
	AnswerEvent.java \
	Event.java \
	Node.java \
	Question.java \
	QuestionEvent.java \
	QuestionGenerator.java \
	RelayEvent.java \
	Simulator.java \
	TimeInterval.java \
	Main.java 

default: classes

classes: $(CLASSES:.java=.class)

clean:
	        $(RM) *.class

