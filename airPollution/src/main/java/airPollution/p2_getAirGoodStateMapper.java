package airPollution;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

//PM 10 (Item code == 8), PM2.5 (Item code == 9)기준으로 공기 질 ' 좋음 ' 이 가장 많이 측정된 지역은?
// -> PM10 기준 30 이하, PM2.5 기준 15이하 를 골라 (지역, 1) 을 emit
public class p2_getAirGoodStateMapper extends Mapper<Object, Text, Text, IntWritable>{
	Text measureDate = new Text(), stationCode = new Text(), instrument = new Text();
	IntWritable val = new IntWritable(1);
	@Override
	protected void map(Object key, Text value, Mapper<Object, Text, Text, IntWritable>.Context context) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		StringTokenizer st = new StringTokenizer(value.toString(), ",");

		// 측정일자, 지역코드, item코드, 값, .. 이 차례대로 들어옴
		measureDate.set(st.nextToken());
		stationCode.set(st.nextToken());
		int itemcode = Integer.parseInt(st.nextToken());
		float averVal = Float.parseFloat(st.nextToken());
		instrument.set(st.nextToken());
		
		if ((itemcode == 8 && averVal <= 30) || (itemcode == 9 && averVal <= 15)) context.write(stationCode, val);
	}
}
