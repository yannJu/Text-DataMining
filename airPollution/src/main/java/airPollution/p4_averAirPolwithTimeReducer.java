package airPollution;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

//시간대에 따라 들어온 아이템 코드와, val을 받아서 공기별 평균과 전체 평균을 출력
public class p4_averAirPolwithTimeReducer extends Reducer<Text, Text, Text, Text> {
	@Override
	protected void reduce(Text key, Iterable<Text> value,
			Reducer<Text, Text, Text, Text>.Context context) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		//시간대, <아이템코드\t값, ...> 과 같이 들어옴
		String itemCode, all, valresult = "";
		Float aveVal;
		Map<String, ArrayList<Float>> maps = new HashMap<String, ArrayList<Float>>();
		Map<String, Float> sumMaps = new HashMap<String, Float>();
		Text valResult = new Text();
		
		for (Text t : value) {
			all = t.toString();
			StringTokenizer st = new StringTokenizer(all, "\t");
			
			itemCode = st.nextToken();
			aveVal = Float.parseFloat(st.nextToken());
			
			ArrayList<Float> values = new ArrayList<Float>();
			if (maps.containsKey(itemCode)) values = maps.get(itemCode);
			values.add(aveVal);
			maps.put(itemCode, values);
		}
		
		for (String k : maps.keySet()) {
			float sum = 0;
			int count = 0;
			ArrayList<Float> averValsLst = maps.get(k);
			for (Float averV : averValsLst) {
				sum += averV;
				count += 1;
			}
			sumMaps.put(k, sum / count);
		}
		
		int allCount = 0;
		float allSum = 0;
		
		for (String aK : sumMaps.keySet()) {
			float tmp = sumMaps.get(aK);
			valresult += "[" + aK + " : " + tmp + "] ";
			allCount += 1;
			allSum += tmp;
		}
		
		valresult += "[All : " + allSum / allCount + "]";
		valResult.set(valresult);
		
		context.write(key, valResult);
	}
}
