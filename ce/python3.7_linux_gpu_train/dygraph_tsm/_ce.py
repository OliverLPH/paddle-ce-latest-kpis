# this file is only used for continuous evaluation test!

import os
import sys
sys.path.append(os.environ['ceroot'])
from kpi import CostKpi, AccKpi

loss_card1_kpi = CostKpi(
    'loss_card1', 0.08, 0, actived=True, desc='train cost')
acc1_card1_kpi = AccKpi(
    'acc1_card1',
    0.08,
    0,
    actived=True,
    desc='train accuracy in one GPU card')

loss_card8_kpi = CostKpi(
    'loss_card8', 0.08, 0, actived=True, desc='train cost')
acc1_card8_kpi = AccKpi(
    'acc1_card8',
    0.08,
    0,
    actived=True,
    desc='train accuracy in 8 GPU card')
tracking_kpis = [
    loss_card1_kpi, 
    acc1_card1_kpi,
    loss_card8_kpi,
    acc1_card8_kpi 
]


def parse_log(log):
    '''
    This method should be implemented by model developers.
    The suggestion:
    each line in the log should be key, value, for example:
    "
    loss_card1\t1.0
    acc1_card1\t1.0
    loss_card8\t1.0
    acc1_card8\t1.0
    "
    '''
    for line in log.split('\n'):
        fs = line.strip().split('\t')
        print(fs)
        if len(fs) == 3 and fs[0] == 'kpis':
            kpi_name = fs[1]
            kpi_value = float(fs[2])
            yield kpi_name, kpi_value


def log_to_ce(log):
    kpi_tracker = {}
    for kpi in tracking_kpis:
        kpi_tracker[kpi.name] = kpi

    for (kpi_name, kpi_value) in parse_log(log):
        print(kpi_name, kpi_value)
        kpi_tracker[kpi_name].add_record(kpi_value)
        kpi_tracker[kpi_name].persist()


if __name__ == '__main__':
    log = sys.stdin.read()
    log_to_ce(log)
