#### TFData

This is a simple package designed for Trounceflow. Please contact wp.trounceflow.com for use of API



Set up

```
curl - ''
pip install ... 
```



To use 

```
import tfdata as tf 
A = tf.APIClient('username', 'password')
A.get_resource(tickers=['CHN:em-bonds','COL:em-bonds','IND:bbg'])
```



Ticker style

Country code: data type

Data type: 

- em-bonds
- bbg