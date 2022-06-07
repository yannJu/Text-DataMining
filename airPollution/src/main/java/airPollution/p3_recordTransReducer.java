package airPollution;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

// "시간\t지역", "itemCode\tVal" 형태로 들어올때, itemCode별로 모아서 출력
public class p3_recordTransReducer extends Reducer<Text, Text, Text, Text>{
	@Override
	protected void reduce(Text key, Iterable<Text> value, Reducer<Text, Text, Text, Text>.Context context) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		String tmpVal, itemCode, valresult = "";
		Float aveVal;
		Text keyResult = new Text(), valResult = new Text();

		//itemCode 별로 aveVal 묶기
		Map<String, Float> maps = new HashMap<String, Float>();
		for (Text val : value) {			
			tmpVal = val.toString();
			StringTokenizer st = new StringTokenizer(tmpVal, "\t");
			
			itemCode = st.nextToken();
			aveVal = Float.parseFloat(st.nextToken());
			
			maps.put(itemCode, aveVal);
		}
		
		keyResult = key;
		for (String k : maps.keySet()) {
			float ave = maps.get(k);
			//[itemCode : val] 와 같이 출력
			valresult += "[" + k + " : " + ave + "] ";
		}
		valResult.set(valresult);
		context.write(keyResult, valResult);
	}
}
