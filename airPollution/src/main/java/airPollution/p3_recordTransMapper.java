package airPollution;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

// <시간, 지역> 별로 묶은 후 측정치 모으기 -> map에서 먼저 <시간, 지역> 대로 묶고 측정치를 출 
public class p3_recordTransMapper extends Mapper<Object, Text, Text, Text> {
	Text dateTime = new Text(), stationCode = new Text(), keyText = new Text(), valText = new Text();
	IntWritable itemCode = new IntWritable();
	FloatWritable averVal = new FloatWritable();
	String tmp, keyTmp, valTmp;
	int cnt = 0;
	
	@Override
	protected void map(Object key, Text value, Mapper<Object, Text, Text, Text>.Context context) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		StringTokenizer st = new StringTokenizer(value.toString(), ",");
		
		if (cnt++ > 0) {
			dateTime.set(st.nextToken());
			stationCode.set(st.nextToken());
			itemCode.set(Integer.parseInt(st.nextToken()));
			averVal.set(Float.parseFloat(st.nextToken()));
			tmp = st.nextToken();
			
			if (Integer.parseInt(tmp.toString()) == 0) {
				keyTmp = dateTime + "->" + stationCode;
				valTmp = itemCode + "\t" + averVal;
				
				keyText.set(keyTmp);
				valText.set(valTmp);
				
				context.write(keyText, valText);
			}
		}
	}
}
