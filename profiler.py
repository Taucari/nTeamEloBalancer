import cProfile, pstats
from main import main
from datetime import datetime
import os


def profile_run():
    main()


if __name__ == '__main__':
    e = datetime.now()
    file_name = '%s-%s-%s %s_%s_%s.txt' % (e.day, e.month, e.year, e.hour, e.minute, e.second)
    save_path = 'profiler_logs'
    cProfile.run('profile_run()', 'output.dat')
    with open(os.path.join(save_path, file_name), 'w') as f:
        p = pstats.Stats('output.dat', stream=f)
        p.sort_stats('time').print_stats()
