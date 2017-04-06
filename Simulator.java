
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;


public class Simulator {
	public static Simulator simulator = new Simulator();
	// simulation time
	long curTime;
	Map<Long, ArrayList<Event>> events; // <Time, Event>
	public Map<String, Node> wholeGraph;
	PrintWriter output;
	PrintWriter question_info;
	PrintWriter user_info;
	static long PoissonArrivalRate=60*60;//sec
	QuestionGenerator questionGenerator;
	List<Question> list_of_question;
	int algorithm = 0; // 0:bottlenect, 1:iASK, 2:SOS
	int random_seed = 0;
	double predictability = 1.0; // {0.6, 0.8, 1}
	int num_of_answerers = 4; // {1, 2, 4, 6, 8}
    double user_asking_rate = 1/4; // {1/10, 1/8, 1/4, 1/2, 1}
    int num_of_expertises = 4; // {2, 4, 8, 16}
    long simulator_last = 3600*24*7; // 7 days
    
    
	public Simulator() {
		list_of_question = new ArrayList<Question>();
		wholeGraph = new HashMap<String, Node>();
		try {
			questionGenerator = new QuestionGenerator();
		} catch (IOException e2) {
			e2.printStackTrace();
		}
		events = new TreeMap<Long, ArrayList<Event>>();
	}
	public void setAskingRate(int index) { /// 0 ~ 4
		double[] rates = {1.0/10.0, 1.0/6.0, 1.0/4.0, 1.0/2.0, 1.0};
		user_asking_rate = rates[index];
		this.PoissonArrivalRate = (long) ((long) 3600 * (1.0/user_asking_rate));
		//System.out.println(1.0/user_asking_rate);
		//System.out.println(this.PoissonArrivalRate);
	}
	public void run() {
		Iterator<Long> it = events.keySet().iterator();
		boolean timesup = false;
		while(it.hasNext()) {
			long key = it.next();
			curTime = key;
			ArrayList<Event> list_of_events = events.get(key);
			Iterator<Event> it_events = list_of_events.iterator();
			//System.out.println("length of events at the same time: " + list_of_events.size());
			while(it_events.hasNext()) {
				Event event = it_events.next();
				event.exec();
				//System.out.println("time: " + event.time);
				if(event.time > this.simulator_last) {
					timesup = true;
					//break;
				}
				it_events.remove();
			}
			if(timesup) {
				//break;
			}
			events.remove(key);
			it = events.keySet().iterator();
		}
		output.close();
		this.printQuestionInfo();
		this.printUserInfo();
	}
	public void addEvent(Event event){
		if(events.get(event.time) == null) {
			events.put(event.time, new ArrayList<Event>());
		}
		events.get(event.time).add(event);
	}
//	public void generateQuestions(int num) {
//		this.num_question = num;
//		for(int i=1; i<=num; i++) {
//			Question q = questionGenerator.generate(i, wholeGraph.size(), random_seed+1);
//			QuestionEvent question_event = new QuestionEvent(q, q.timeInterval.startingTime*3600);
//			if(events.get(question_event.time) == null) {
//				events.put(question_event.time, new ArrayList<Event>());
//			}
//			events.get(question_event.time).add(question_event);
//			list_of_question.add(q);
//		}
//	}
	public void printQuestionInfo() {
		Iterator<Question> it = list_of_question.iterator();
		
		while(it.hasNext()) {
			Question q = it.next();
			q.solved();
		}
		this.question_info.close();
	}
	public void usersAskQuestion() {
//		Question q = questionGenerator.generate(3, 0, wholeGraph.size(), 24);
//		QuestionEvent q_event = new QuestionEvent(q, 0L);
//		q_event.startingTime = q.timeInterval.startingTime;
//		q_event.endingTime = q.timeInterval.endingTime;
//		if(events.get(q_event.time) == null) {
//			events.put(q_event.time, new ArrayList<Event>());
//		}
//		events.get(q_event.time).add(q_event);
//		list_of_question.add(q);
		Iterator it = wholeGraph.entrySet().iterator();
		int questionId = 0;
		while (it.hasNext()) {
			Map.Entry pair = (Map.Entry) it.next();
			Node asker = (Node) pair.getValue();
			//System.out.println("--------------------------------");
			//System.out.println("ASKER: " + asker.userId);
			long simulator_time = 0L;
			do {
				long nextTime = this.poissonNextTime((1.0/(double)Simulator.PoissonArrivalRate));
				long happeningTime = simulator_time + nextTime;
				//System.out.println("current Time: " + simulator_time);
				//System.out.println("nexttime: " + nextTime);
				Question q = questionGenerator.generate(Integer.parseInt(asker.userIndex), questionId, wholeGraph.size(), (int)happeningTime/3600);
				QuestionEvent q_event = new QuestionEvent(q, simulator_time+nextTime);
				q_event.startingTime = q.timeInterval.startingTime;
				q_event.endingTime = q.timeInterval.endingTime;
				if(events.get(q_event.time) == null) {
					events.put(q_event.time, new ArrayList<Event>());
				}
				events.get(q_event.time).add(q_event);
				list_of_question.add(q);
				simulator_time = happeningTime;
				questionId ++;
			}while(simulator_time <= this.simulator_last);
		}
	}
	public long poissonNextTime(double L) {
		double rand = Math.random();
		//System.out.println((-Math.log(1-rand)/L));  
		return (long) (-Math.log(1.0-rand)/L);
	}
	public void printUserInfo() {
		Iterator it = wholeGraph.entrySet().iterator();
	    while (it.hasNext()) {
	    	Map.Entry pair = (Map.Entry)it.next();
	        ((Node)pair.getValue()).writeToOutput();
	    }
	    this.user_info.close();
	}
	public void getWholeGraph() throws IOException, ParseException {
		BufferedReader br = null;
		BufferedReader br_ad = null;
		String line;
		String[] str;
		Map<String, Node> nodes_time = new HashMap<String, Node>();
		try {
			br = new BufferedReader(new FileReader("1_2_hop_time.csv"));
			br_ad = new BufferedReader(new FileReader("1_2_hop_adjacencylist.csv"));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
		    line = br.readLine();
		    while (line != null) {
		        str = line.split(",");
 		        Node n = new Node();
		        n.userId = str[0];
		        int k = 0;
		        for(int i=1; i<str.length; i++) {
		        	if(k%2==1) {
		        		k++;
		        		continue;
		        	}
		        	Long a_t = Long.parseLong(str[i]);
		        	double rand = Math.random();
		        	if(rand<=predictability) {
		        		n.activeTime.add(a_t);
		        	}
		        	k++;
				}
		        nodes_time.put(str[0], n);
		        //wholeGraph.put(str[0], n);
		        line = br.readLine();
		    }
		    //System.out.println("size: " + wholeGraph.size());
		} finally {
		    br.close();
		}
		Integer i=0; 
		while((line = br_ad.readLine()) != null) {
			str = line.split(",");
			if(nodes_time.containsKey(str[0])) {
				Node n = nodes_time.get(str[0]);
				n.userIndex = i.toString();
				wholeGraph.put(str[0], n);
				i++;
				for(int j=1; j<str.length; j++) {
					String[] edge_delay = str[j].split(": ");
					if(nodes_time.containsKey(edge_delay[0])) {
						n.edge_delay.put(edge_delay[0], Integer.parseInt(edge_delay[1]));
					}
				}
			}
		}
		
		
	}
	
	public void createOutputFiles() {
		try {
			StringBuilder file_name = new StringBuilder();
			
			if(this.algorithm == 0) file_name.append("Bottleneck/").append("Bottleneck_").append(this.PoissonArrivalRate).append("_").append(this.random_seed).append("_").append(this.predictability).append("_").append(this.num_of_expertises);
			else if(this.algorithm == 1) file_name.append("iASK/").append("iASK_").append(this.PoissonArrivalRate).append("_").append(this.random_seed).append("_").append(this.predictability).append("_").append(this.num_of_expertises);
			//else if(this.algorithm == 2) file_name.append("SOS/").append("SOS_").append(this.PoissonArrivalRate).append("_").append(this.random_seed).append("_").append(this.predictability).append("_").append(this.num_of_expertises);
		
			output = new PrintWriter("results/log/" + file_name.toString() + "_log.txt");
			question_info = new PrintWriter("results/questions/" + file_name.toString() + "_question_info.txt");
			user_info = new PrintWriter("results/users/" + file_name.toString() + "_user_info.txt");
		}catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}
	public void setAlgorithm(int i) {
		this.algorithm = i;
	}
}
