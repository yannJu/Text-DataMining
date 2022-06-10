package airPollution;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

// itemCode 가 8인 경우(PM 10)의 지역코드와 값을 emit
public class p1_getAveMaxMinMapper extends Mapper<Object, Text, Text, FloatWritable>{
	Text measureDate = new Text(), stationCode = new Text(), instrument = new Text();
	IntWritable itemCode = new IntWritable();
	FloatWritable averVal = new FloatWritable();
	int cnt = 0;
	@Override
	protected void map(Object key, Text value, Mapper<Object, Text, Text, FloatWritable>.Context context) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		StringTokenizer st = new StringTokenizer(value.toString(), ",");

		if (cnt++ > 0) {
			// 측정일자, 지역코드, item코드, 값, .. 이 차례대로 들어옴
			measureDate.set(st.nextToken());
			stationCode.set(st.nextToken());
			int itemcode = Integer.parseInt(st.nextToken());
			averVal.set(Float.parseFloat(st.nextToken()));
			instrument.set(st.nextToken());
			
			if (itemcode == 8 && Integer.parseInt(instrument.toString()) == 0) {
				itemCode.set(itemcode);
				context.write(stationCode, averVal);
			}
		}
	}
}
