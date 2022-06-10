package airPollution;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

// 시간대(날짜 상관 xx)에 따라 평균 공기질 분석 -> mapper는 시간대에 value를 emit
public class p4_averAirPolwithTimeMapper extends Mapper<Object, Text, Text, Text> {
	Text keyResult = new Text(), valResult = new Text(); //results
	String valresult = "", date = "", time = "", allDATE = "", itemCode = "", aveVal = "";
	
	Text tmp = new Text();
	int cnt = 0;
	
	@Override
	protected void map(Object key, Text value, Mapper<Object, Text, Text, Text>.Context context)
			throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		StringTokenizer st = new StringTokenizer(value.toString(), ",");

		if (cnt++ > 0) {
			// 측정일자, 지역코드, item코드, 값, .. 이 차례대로 들어옴
			allDATE = st.nextToken();
			StringTokenizer dateTK = new StringTokenizer(allDATE);
			
			date = dateTK.nextToken();
			time = dateTK.nextToken();
			keyResult.set(time);
			
			//---
			tmp.set(st.nextToken());//stationCode
			
			itemCode = st.nextToken();//itemCode
			aveVal = st.nextToken(); //averageVal
			tmp.set(st.nextToken());//instrument
			
			if (Integer.parseInt(tmp.toString()) == 0) {
				//---
				valresult = itemCode + "\t" + aveVal;
				valResult.set(valresult);
				
				context.write(keyResult, valResult);
			}
		}
	}
}
