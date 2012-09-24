
import sys
from jsimutils import mean,stddev

nblocks = 5

def block_avg_file():
    lines = sys.stdin.readlines()
    print "%d total values in list" % len(lines)
    column = [ float(line.rstrip('\n')) for line in lines ]
    offset = len(column) % nblocks
    while True:
        block_size = len(column[offset:]) / nblocks
        print "skipping first %d values" % offset
        block_avgs = [ mean(block) for block in list_block(column[offset:], block_size) ]
        if stddev(block_avgs) <  stddev(block_avgs[1:]):
            print "%f +- %f" % (mean(block_avgs), stddev(block_avgs))
            break
        else:
            offset += block_size
        
    return 0

        
def list_block(lst, size):
    """Yields size-sized chunks of list lst.
    """
    for i in range(0, len(lst), size):
        yield lst[i:i+size]


if __name__ == '__main__':
    r = block_avg_file()
    sys.exit(r)

