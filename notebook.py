import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.vstack([
        mo.md("# 5 inch Long Range FPV"),
    ])
    return


@app.cell
def _():
    # %% markdown
    # ## Importing Package Specification from CSV

    # %% code
    from pathlib import Path
    import pandas as pd
    from marimo import md

    # Read CSV
    csv_path = Path("assets") / "package_spec.csv"
    df = pd.read_csv(csv_path)

    # Compute total package weight
    total_weight = df["Weight"].sum()

    # Convert table to markdown
    md_table = df.to_markdown(index=False)

    # Display the table with total weight
    md(f"""
    ### Package Specification

    {md_table}

    **Total Package Weight:** {total_weight:} g
    """)
    return Path, md, pd


@app.cell
def _(mo):
    W = 0.4
    T_hover = W*9.81*1


    mo.md(f"""
    ## Vehicle

    - Weight: {W} kg, снаряженная масса дрона;
    - Hover Thrust: {T_hover:.2f} N, тяга висения T/W=1;

    """)
    return


@app.cell
def _(Path, md, pd):

    # Read CSV
    csv_path2 = Path("assets") / "banchmark.csv"
    df2 = pd.read_csv(csv_path2)

    # Convert table to markdown
    md_table2 = df2.to_markdown(index=False)

    #параметры режима полета "Cruize lite"
    I = 1.27
    f_m = 11000


    # Display the table with total weight
    md(f"""
    ### Banchmark

    {md_table2}

    """)
    return I, f_m


@app.cell
def _(md):
    V_bat = 6*3.7
    R_in = 10/1000
    C_bat = 1300

    md(f"""
    ### Battery

    - Type: Li-Po
    - Voltage: {V_bat:.1f} В, Номинальное напряжение 6s батареи, 3.7В на ячейку;
    - Impedance: {R_in} Ohm
    - Capacity: {C_bat} mAh

    При переходе на Li-Ion 6s:
    - ток на круизе I=1.8A, увеличится на 42%;
    - тяговооруженность T/W снизится с 9.5 до 6.5 на 31%;
    - емкость увеличится на 200%
    - время полета увеличится на 100%;

    При переходе на Li-Ion 5s:
    - при тойже динамике необходимая тяга T=160г, ток I=2.04 A увеличится на 14%;
    - эффективная емкость акб немного ниже из-за провала ВАХ (не учитывается);
    - по сравнению с 6s время полета  уменьшится на 12%, T/W улучшится на 1%;
    - переход на 5s нецелесообразен из-за возрастания тока;

    """)
    return (V_bat,)


@app.cell
def _(P_motor, f_m, mo, pi, sqrt):

    D = 5.1*25.4/1000
    A = pi*pow(D, 2)/4
    pitch = 2.6
    FM = 0.8

    P_ind = P_motor*FM
    T = pow(P_ind*sqrt(2*1.2*A), 2/3)/9.81*1000

    c = pi*D
    t = f_m/60
    vilocity = pi*D*f_m/60


    mo.md(f"""
    ## Props

    - Prop Diameter: {D*1000:.1f} mm, диаметр винта;
    - Prop area: {A*10000:.1f} кв.см, площадь диска;
    - Pitch: {pitch} inch, шаг винта - продольное перемещение на один оборот;
    - При меньшем шаге меньше “pitch speed”, для создания той же тяги требуется больше оборотов, но меньше момента и тока.
    - Переход с 2-лопастного на 3-лопастный винт тяга увеличится на ~10–25%, ток и мощность возрастут на ~15–35%. Целесообразно, если занижен Kv, не хватает тяги на верхах.
    - Figure of merit: {FM}, качества винта
    - Power: {P_ind:.2f}, идуцированная мощность
    - Thrust: {T:.0f} грамм, проверка рассчета - совпадает с бенчмарком!
    - Линейная скорость винта: {vilocity:.0f} м/с, для оценки шумов и снижения КПД из-за турбулентности;
    - В относительных единицах: {vilocity/343:.1f} мах, ниже критической зоны (0.6–0.8);

    """)
    return


@app.cell
def _(I, V_bat, f_m, mo, pi):

    #параметры двигателя
    motor_size = pow(21, 2)*4
    I_idle = 0.5
    efficiency = 0.86
    Kv = 1800
    V = V_bat
    n_max0 = V * Kv
    n_max = n_max0 * 0.8
    Kt = 60/(2*pi*Kv)

    omega = 2*pi*f_m/60
    M_motor = Kt*I*efficiency
    P_motor = M_motor*omega
    E_emf = omega/Kt


    mo.md(f"""
    ## Motors - 2104, 1800kv
    - Motor type: BLDC
    - Motor size: {motor_size}, объем двигателя в условных единицах для сравнения с другими моторами;
    - Idle current: {I_idle} A, ток холостого хода мотора, растет с ростом Kv
    - Efficiency: {efficiency}, КПД по паспорту, при токах 0.6-2.0А;
    - Kv: {Kv} rpm/V, равно скорости вращения, на которой ЭДС мотора (back-EMF) составит 1В. Обратно пропорционален магнитному потоку Ф;
    - No-load RPM: {n_max0:.0f}, максимальные обороты на холостом ходу, ограничен противо-ЭДС мотора;
    - Actual RPM: {n_max:.0f}, фактическая максимальныая скорость условно меньше на 20% из-за потерь;
    - K_torque: {Kt:.4f} N\\*m/A, коэффициент крутящего момента. Kv\\*Kt=9.55 (прибл.);

    - Frequency: {f_m} rmp, частота вращения механическая в выбранном режиме полета;
    - Угловая скорость {omega:.0f} rad/sec;
    - Крутящий момент: {M_motor:.3f} N*m;
    - Back-EMF: {E_emf:.1f} at {f_m} rpm;
    - Ток определяется активным сопротивлением цепи и противо-ЭДС: V=E_emf + IR;
    - При чрезмерной нагрузке ESC поднимает фазное V, a Eemf падает с оборотами. Как следвие, ток потерь возрастает;
    - Для обеспечения заданных оборотов при высокой нагрузке выгоден низкий Kv, т.к. мотор обладает большим моментом. Мотор с высоким Kv при этом не даст достаточный противо-ЭДС, из-за чего возникнет высокий ток потерь.
    - Метрика Eemf/V<0.8, важно что оценка валидна только для 100% "газа", когда фазное напряжение максимально Eesc=V;
    - Оценка потерь:  P_el=VI; P_mech=M\\*omega=E\\*I; V_margin=V-E; P_loss=P_el-P_mech=V_margin\\*I; 
    - Потери на внутреннем сопротивлении: Pres=I2*(Rmotor+Resc+Rbattery);
    - Магнитные потери: Pcore=Ploss-Pres. Оценка по току хх на различных P(omega)->omega^alfa, где alfa[1.5-2] вычислить по трем точкам;
    - Индуктивность катушки U=L\\*dI/dt;


    """)
    return P_motor, omega


@app.cell
def _(f_m, mo, omega):
    #setup axes
    N_p = 7
    f_e = N_p*f_m;

    L = 20*pow(10, -6)
    R_loop = 210*pow(10, -3)+0.01
    tan_fi = omega*L/R_loop

    mo.md(f"""
    ## ESC

    - Motor poles: {N_p}, количество пар полюсов
    - Electrical frequency: {f_e} rpm
    - Duty cycle: D, заполнение фазного импульса. V = D\\*V_bat;
    - При малом заполнении D<30% ток становится импульсным, из-за чего КПД сильно падает
    - Полная мощность S = P + jQ, P=UI\\*cos(fi), Q=UI\\*sin(fi);
    - tan(fi) = omega\\*L/R = {tan_fi:.2f}, то есть реактивная состовляющая растет вместе с частотой omega;

    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from math import pi
    from math import sqrt
    return mo, pi, sqrt


if __name__ == "__main__":
    app.run()
