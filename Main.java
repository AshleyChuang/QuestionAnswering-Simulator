import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class Main {
	
	public static void main(String[] args) throws IOException, ParseException {
		Simulator.simulator.setAlgorithm(Integer.parseInt(args[0]));
		Simulator.simulator.setAskingRate(Integer.parseInt(args[1]));
		Simulator.simulator.random_seed = Integer.parseInt(args[2]);
		Simulator.simulator.predictability = Double.parseDouble(args[3]);
		Simulator.simulator.num_of_expertises = Integer.parseInt(args[4]);
		Simulator.simulator.getWholeGraph();
		Simulator.simulator.usersAskQuestion();
		Simulator.simulator.createOutputFiles();
		Simulator.simulator.run();
	}
}
