import toml
import time
import os
import shutil

colocations = toml.load("collocations.toml")
config = toml.load("weaver.toml")

user_count = 6000
user_spawn = 90
host = "localhost:12345"
memory = "10g"
cpus = "4"
run_time = "180s"
weaver_cpu = "20"

results_folder_name = "results-99"

#  sudo env "PATH=$PATH" python auto_test.py

for (service, colocate) in colocations.items():
    # os.system("weaver multi purge --force")
    shutil.rmtree(service, ignore_errors=True)
    os.makedirs(service, exist_ok=True)
    os.chdir(service)
    file = open("weaver.toml", "a")
    config['serviceweaver']['colocate'] = colocate['colocate']
    toml.dump(config, file)
    file.close()
    shutil.copyfile("../locustfile.py", "locustfile.py")
    # os.system("weaver multi deploy weaver.toml &")
    # time.sleep(5)

    # limitar o consumo de CPU do Weaver pra induzir falha na aplicação
    # weaver_pid = subprocess.check_output(["pidof", "weaver"])
    # print(f"pid do weaver: {int(weaver_pid)}")
    os.system("echo 'weaver multi deploy weaver.toml' > deploy.sh")
    os.system("chmod +x deploy.sh")
    os.system("ulimit -n 500000")
    os.system(f'systemd-run --scope -p CPUQuota={weaver_cpu}% ./deploy.sh &')

    # os.system(f"cpulimit -i --pid={int(weaver_pid)} -l={weaver_cpu} &")

    time.sleep(3)

    # Realizar teste de carga 
    os.system(f"locust --host='http://{host}' --headless --run-time={run_time} -u '{user_count}' -r {user_spawn} 2>&1 --csv=results")

    # Finalizar processo do weaver
    os.system("weaver multi purge --force")
    time.sleep(10)
    print(f"finalizados os testes no serviço {service}!")
    time.sleep(5)
    os.chdir("..")

os.makedirs(results_folder_name, exist_ok=True)
os.makedirs(f"{results_folder_name}/cpu-{weaver_cpu}", exist_ok=True)
os.system(f"mv service1 {results_folder_name}/cpu-{weaver_cpu}")
os.system(f"mv service2 {results_folder_name}/cpu-{weaver_cpu}")
os.system(f"mv service3 {results_folder_name}/cpu-{weaver_cpu}")

print("Testes finalizados! :)")
