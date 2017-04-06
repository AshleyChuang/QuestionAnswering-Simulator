import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;

public class QuestionGenerator{
	List<String> keywords;
	
	public QuestionGenerator() throws IOException {
		keywords = new ArrayList<String>();
		BufferedReader br = null;
		try {
			br = new BufferedReader(new FileReader("dataset/keywords.txt"));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
		    String line = br.readLine();
		    
		    while (line != null) {
		        keywords.add(line);
		        line = br.readLine();
		    }
		} finally {
		    br.close();
		}
	}
	
	public Question generate(Integer askerId, Integer questionId, int size, int starting_time) {
		Question q = null;
		long seed = Simulator.simulator.random_seed+questionId;
		Random random = new Random();
		random.setSeed(seed);
		int num_of_keywords = Simulator.simulator.num_of_expertises;
		
		int source_index = askerId;
		int num_of_answerers = Simulator.simulator.num_of_answerers;
		int start_time = starting_time%24;
		int end_time = 20;//(int) random.nextInt(24)+1;
        if(start_time==0) start_time = 24;
		while(end_time == start_time) {
			end_time = (int) random.nextInt(24)+1;
		}
		StringBuilder str = new StringBuilder();
		for(int i=0; i<num_of_keywords; i++) {
			str.append(keywords.get(i)+" ");
		}
		
		TimeInterval timeInterval = new TimeInterval(start_time, end_time);
		Object[] nodes = Simulator.simulator.wholeGraph.values().toArray();
		q = new Question(questionId.toString(), ((Node)nodes[source_index]), num_of_answerers, str.toString(), timeInterval);
//		System.out.println("starting time: " + start_time + ", ending time: " + end_time);
//		System.out.println("source: " + source_index + ", num of answerers: " + num_of_answerers);
//		System.out.println("Question: " + str.toString());
		return q;
	}
}
