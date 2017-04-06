import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;


public class Node {
	boolean source; 
	boolean target;
	boolean passer;
	String userId;
	String userIndex;
	long getQuestionTime;
	long answeringTime;
	long getQuestionPeriod;
	int times_pass;
	int times_answer;
	ArrayList<Node> pass_to;
	ArrayList<Long> activeTime;
	ArrayList<Long> askerActiveTime;
	Map<Long, Integer> pass_each_day;
	Map<Long, Integer> answer_each_day;
	Map<String, Integer> edge_delay;
	
	public Node() throws ParseException{
		source = false;
		target = false;
		passer = false;
		times_pass = 0;
		//getQuestionTime = getQuestionTime.p
		answeringTime = (long)0;// 1 hour
		pass_to = new ArrayList<Node>();
		activeTime = new ArrayList<Long>();
		pass_each_day = new HashMap<Long, Integer>();
		answer_each_day = new HashMap<Long, Integer>();
		edge_delay = new HashMap<String, Integer>();
	}
	
	public void writeToOutput() {
		List<Integer> average_pass = new ArrayList<Integer>();
		List<Integer> average_answer = new ArrayList<Integer>();
		Double a_p = 0.0;
		Double a_a = 0.0;
		
		Iterator it = pass_each_day.entrySet().iterator();
	    while (it.hasNext()) {
	    	Map.Entry pair = (Map.Entry)it.next();
	    	average_pass.add((Integer) pair.getValue());
	    }
	    
	   	it = answer_each_day.entrySet().iterator();
	    while (it.hasNext()) {
	    	Map.Entry pair = (Map.Entry)it.next();
	    	average_answer.add((Integer) pair.getValue());
	    }
	    
	    Integer sum = 0;
	    if(!average_pass.isEmpty()) {
	      for (Integer p :average_pass) {
	          sum += p;
	      }
	      a_p = sum.doubleValue() / average_pass.size();
	    }
	    sum = 0;
	    if(!average_answer.isEmpty()) {
	      for (Integer a :average_answer) {
	          sum += a;
	      }
	      a_a = sum.doubleValue() / average_answer.size();
	    }
	    
		Simulator.simulator.user_info.println(userId + "," + Integer.toString(times_pass) + "," + Integer.toString(times_answer) + "," + a_p.toString() + ", " + a_a.toString()  + "," + Integer.toString(pass_to.size()));
	}
}
