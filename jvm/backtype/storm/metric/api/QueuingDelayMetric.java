/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package backtype.storm.metric.api;

import backtype.storm.metric.api.IMetric;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.lang.System;

public class QueuingDelayMetric implements IMetric {
    private final Logger LOG = LoggerFactory.getLogger(QueuingDelayMetric.class);
    double sum;
    int cnt;
    String name;
    String name_bolt;
    long cal_rate;
    long prev_time;
    int queue_count=0;

    public QueuingDelayMetric(String executor_id, String component_id) {
        sum = 0.0;
        cnt = 0;
        name = new String(executor_id);
        name_bolt=new String(component_id);
    }


    public void update(double queuing_delay) {
        sum += queuing_delay;
        cnt++;


            Object val = queuing_delay;
            LOG.info("RecvQDelay: " + queuing_delay + " " + System.currentTimeMillis() + " " + name+" "+name_bolt);

    }

    public Object getValueAndReset() {
        double ret = sum/cnt;
        sum = 0.0;
        cnt = 0;
        return ret;
    }
}
