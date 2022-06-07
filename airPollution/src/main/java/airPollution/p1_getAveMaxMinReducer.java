package airPollution;

import java.io.IOException;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class p1_getAveMaxMinReducer extends Reducer<Text, FloatWritable, Text, Text>{
	String result = "";
	Text resultTxt = new Text();
	@Override
	protected void reduce(Text stationCode, Iterable<FloatWritable> values,
			Reducer<Text, FloatWritable, Text, Text>.Context context) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		int cntVal = 0;
		float sum = 0, maxVal = Float.MIN_VALUE, minVal = Float.MAX_VALUE;
		for (FloatWritable value : values) {
			float val = value.get();
			maxVal = Math.max(maxVal, val);
			minVal = Math.min(minVal, val);
			sum += val;
			cntVal += 1;
		}
		
		result = "Aver : " + (sum / cntVal) + "\tMax : " + maxVal + "\tMin " + minVal;
		resultTxt.set(result);
		context.write(stationCode, resultTxt);
	}
}