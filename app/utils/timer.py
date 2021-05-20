from datetime import datetime, date, timedelta

class CountDownTimer():

	def __init__(self, master, str_time) -> None:
		
		self.master = master
		self.str_time = str_time
		self.str_time.set('Timer: 15:00')

	def get_h_m(self, timedelta_obj):

		m, s = str(timedelta_obj).split('.')[0].split(':')[1:]
		return m, s

	def start(self):

		self.stop = False
		self.end_time = (datetime.now() + timedelta(minutes=15)).time()
		self.update()

	def update(self):

		if self.stop:
			return

		now = datetime.now().time()
		duration = datetime.combine(date.min, self.end_time) - datetime.combine(date.min, now)
		m, s = self.get_h_m(duration)
		self.str_time.set('Timer: %2s:%2s' % (m, s))

		self.master.after(1000, self.update)

	def stop_and_reset(self):

		self.stop = True
		self.str_time.set('Timer: 15:00')
