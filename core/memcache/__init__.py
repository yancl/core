import cmemcached

def get_new_mc_instance(hosts):
    mc = cmemcached.Client(hosts, comp_threshold=256, comp_method='quicklz')
    mc.set_behavior(cmemcached.BEHAVIOR_BINARY_PROTOCOL, 1)
    return mc
