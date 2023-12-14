import sys
sys.path.append("/home/etelvinaoliveira")

def handler(input_dict, context):
  outgoing_traffic_bytes = input_dict['net_io_counters_eth0-bytes_recv'] / (input_dict['net_io_counters_eth0-bytes_sent'] + input_dict['net_io_counters_eth0-bytes_recv'])

  percentage_memory_caching_content = (input_dict['virtual_memory-buffers'] + input_dict['virtual_memory-cached']) /(input['virtual_memory-total'])

  percents = []
  dictResult = {}

  dictResult['outgoing_traffic_bytes'] = outgoing_traffic_bytes
  dictResult['percentage_memory_caching_content'] = percentage_memory_caching_content

  for (key, value) in input_dict.items():
    if "cpu_percent" in key:
      percents.append(value)
      if context.env.get(f"list_{key}") is None:
        context.env[f"list_{key}"] = [value]
      else:
        if len(context.env[f"list_{key}"]) < 12:
          context.env[f"list_{key}"].append(value)
        else:
          context.env[f"list_{key}"][:10] = context.env[f"list_{key}"][1:]
          context.env[f"list_{key}"][11] = value

  for (key, value) in context.env.items():
    if "list_cpu_percent" in key:
      sumValues = sum(value)
      mean = sumValues / len(value)
      numCpu = key.split("-")[-1]
      dictResult[f"avg-util-cpu{numCpu}-60sec"]

  return dictResult
