import java.util.Date;
import java.util.Iterator;


public class RelayEvent extends Event{
	Node relay_node;
	long period;
	Question q;
	
	public RelayEvent(Question q, Node relay_node, long time, long pd) {
		q.number_pass++;
		this.q = q;
		this.time = time;
		this.period = pd;
		relay_node.times_pass += 1;
		this.relay_node = relay_node;
		relay_node.getQuestionTime = time;
		relay_node.getQuestionPeriod = pd;
	}
	
	public void exec() {
		//System.out.println(q.questionId + " relaynode "  + relay_node.userId + " : " + Long.toString(time));
		Simulator.simulator.output.println(q.questionId + " passer " + relay_node.userId + " : " + Long.toString(time));
		super.exec();
	}
}
