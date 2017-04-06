

public class AnswerEvent extends Event{
	Node target;
	long period;
	Question q;
	
	public AnswerEvent(Question q, Node target_node, long time, long pd) {
		q.number_answer++;
		this.q = q;
		this.time = time;
		this.period = pd;
		target_node.times_answer += 1;
		this.target = target_node;
		q.spentTime.add(period + target.answeringTime);
	}
	
	public void exec() {
		//System.out.println(q.questionId + " answerer "  + target.userId + " : " + Long.toString(time + target.answeringTime));
		Simulator.simulator.output.println(q.questionId + " answerer "  + target.userId + " : " + Long.toString(time+ target.answeringTime));
		//q.spentTime.add(period + target.answeringTime);
		super.exec();
	}
}
