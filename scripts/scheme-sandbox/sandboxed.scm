(use srfi-1 posix sandbox)

(define env (make-safe-environment parent: default-safe-environment
                                   mutable: #t
                                   extendable: #t)) 

(define (sandbox-eval str)
  (safe-eval str
             fuel: 10000
             environment: env
             allocation-limit: 1000000))

(define (eval-input)
  (let ((results (port-map sandbox-eval read)))
    (printf "~S" (last results))))

(with-input-from-port (open-input-file* fileno/stdin) eval-input)
