package airPollution;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

// 들어온 지역의 수를 count 하여 가장 count 가 큰 지역을 출력 ~> 지역들을 count 후 간단한 스크립트 파일을 이용하여 한가지 지역을 뽑음.
// 즉 reduce 는 지역 conunt 만!
public class p2_getAirGoodStateReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
	IntWritable result = new IntWritable();
	@Override
	protected void reduce(Text key, Iterable<IntWritable> value,
			Reducer<Text, IntWritable, Text, IntWritable>.Context context) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		int sum = 0;
		for (IntWritable val : value) {
			sum += val.get();
		}
		
		result.set(sum);
		context.write(key, result);
	}
}
