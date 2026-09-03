# app.py
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_key_needed_for_sessions'

@app.route('/')
def index():
    last_hours = session.get('last_hours')
    last_money = session.get('last_money')
    return render_template('index.html', last_shift_hours=last_hours, last_shift_money=last_money)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get hourly wage and time inputs from form
    wage = float(request.form.get('wage', 0))
    start_str = request.form.get('start_time')
    end_str = request.form.get('end_time')
    
    # Save wage to session for persistence
    session['wage'] = wage
    
    # Parse times
    start_hour, start_min = map(int, start_str.split(':'))
    end_hour, end_min = map(int, end_str.split(':'))
    
    start_total_mins = start_hour * 60 + start_min
    end_total_mins = end_hour * 60 + end_min
    
    # Handle overnight shifts
    if end_total_mins < start_total_mins:
        end_total_mins += 24 * 60
        
    # Calculate current shift metrics
    shift_hours = (end_total_mins - start_total_mins) / 60
    shift_money = shift_hours * wage
    
    # Save last shift for display
    session['last_hours'] = shift_hours
    session['last_money'] = shift_money
    
    # Accumulate running totals for the month
    session['total_hours'] = session.get('total_hours', 0) + shift_hours
    session['total_money'] = session.get('total_money', 0) + shift_money
    
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('total_hours', None)
    session.pop('total_money', None)
    session.pop('last_hours', None)
    session.pop('last_money', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
