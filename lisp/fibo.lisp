(defun fibonacci-series (n)
  "Generates a list of the first N Fibonacci numbers iteratively."
  (loop :for a := 0 :then b
        :and b := 1 :then (+ a b)
        :repeat n
        :collect a))

(format t "Enter the number of Fibonacci elements: ")
(finish-output) ; Ensures the prompt appears immediately

(let ((input (read)))
  (if (numberp input)
      (format t "Series: ~A~%" (fibonacci-series input))
      (format t "Please enter a valid number.~%")))