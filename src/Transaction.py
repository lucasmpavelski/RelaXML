from threading import RLock


def transaction_with_lock(lock_name, log_name):
    """ Decorate as a thread-exclusive method and stores the log. """
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            log_path = getattr(self, log_name)
            if lock != None :
                with lock:
                    log = open(log_path, 'a')
                    log.write(method.__name__ + " - " + str(args) + "\n")
                    r = method(self, *args, **kws)
                    log.close()
            else :
                log = open(log_path, 'a')
                log.write(method.__name__ + "\n")
                r = method(self, *args, **kws)
                log.close()
            return r
        return synced_method 
    return decorator
