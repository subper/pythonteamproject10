<?php
    if(!$_GET['s']){$s=date("Y-m-d");} // 오늘날짜를 구합니다. $s 에 넣습니다.
    else{$s=$_GET['s'];}

    function crd($s){ // 함수를 제작합니다. 함수내에서 변수 $s 는 "지정된 달" 입니다 
        $x=explode("-",$s); // 들어온 날짜를 년,월,일로 분할해 변수로 저장합니다.
        $s_Y=$x[0]; // 지정된 년도 
        $s_m=$x[1]; // 지정된 월
        $s_d=$x[2]; // 지정된 요일

        $today=explode("-",date("Y-m-d")); // 들어온 날짜를 년,월,일로 분할해 변수로 저장합니다.
        $t_Y=$today[0]; // 지정된 년도 
        $t_m=$today[1]; // 지정된 월
        $t_d=$today[2]; // 지정된 요일
         
        $s_t=date("t",mktime(0,0,0,$s_m,$s_d,$s_Y)); // 지정된 달은 몇일까지 있을까요?
        $s_n=date("N",mktime(0,0,0,$s_m,1,$s_Y)); // 지정된 달의 첫날은 무슨요일일까요?
        $l=$s_n%7; // 지정된 달 1일 앞의 공백 숫자.
        $ra=($s_t+$l)/7; $ra=ceil($ra); $ra=$ra-1; // 지정된 달은 총 몇주로 라인을 그어야 하나?
         
        $n_d= date("Y-m-d",mktime(0,0,0,$s_m,$s_d+1,$s_Y)); // 다음날
        $p_d= date("Y-m-d",mktime(0,0,0,$s_m,$s_d-1,$s_Y)); // 이전날
        $n_m= date("Y-m-d",mktime(0,0,0,$s_m+1,$s_d,$s_Y)); // 다음달 (빠뜨린 부분 추가분이에요)
        $p_m= date("Y-m-d",mktime(0,0,0,$s_m-1,$s_d,$s_Y)); // 이전달
        $n_Y= date("Y-m-d",mktime(0,0,0,$s_m,$s_d,$s_Y+1)); // 내년
        $p_Y= date("Y-m-d",mktime(0,0,0,$s_m,$s_d,$s_Y-1)); // 작년    

    // 변수 $s 에 새로운 값을 넣고 새문서를 만들면, $s 가 들어와 원하는 값을 표시해 줍니다.
    echo ("
        <table style='border: 1px solid #bcbcbc;'>
            <tr>
              <td colspan=2 width='160px' style='border-left: 1px solid #bcbcbc; border-top: 1px solid #bcbcbc; border-bottom: 1px solid #bcbcbc; text-align: center;'><div style='font-weight:bold; font-size:20px;'><a href='calender.html?s=$p_m'>◀◀</a></div></td>
              <td width='240px' align=center colspan=3 style='border-top: 1px solid #bcbcbc; border-bottom: 1px solid #bcbcbc;'><div style='font-weight:bold; font-size:20px;'>$s_Y 년 $s_m 월</div></td>
              <td colspan=2 width='160px' align=center style='border-right: 1px solid #bcbcbc; border-top: 1px solid #bcbcbc; border-bottom: 1px solid #bcbcbc; text-align: center;'><div style='font-weight:bold; font-size:20px;'><a href='calender.html?s=$n_m'>▶▶</a></div></td>
            </tr>
            <tr>
                <td width='80px' style='border: 1px solid #bcbcbc; text-align: center;'>일요일</td>
                <td width='80px' style='border: 1px solid #bcbcbc; text-align: center;'>월요일</td>
                <td width='80px' style='border: 1px solid #bcbcbc; text-align: center;'>화요일</td>
                <td width='80px' style='border: 1px solid #bcbcbc; text-align: center;'>수요일</td>
                <td width='80px' style='border: 1px solid #bcbcbc; text-align: center;'>목요일</td>
                <td width='80px' style='border: 1px solid #bcbcbc; text-align: center;'>금요일</td>
                <td width='80px' style='border: 1px solid #bcbcbc; text-align: center;''>토요일</td>
            </tr>
        ");
        for($r=0;$r<=$ra;$r++){
            echo "<tr>";
                for($z=1;$z<=7;$z++){
                    $rv=7*$r+$z; $ru=$rv-$l; // 칸에 번호를 매겨줍니다. 1일이 되기전 공백들 부터 마이너스 값으로 채운 뒤 ~ 
                    echo "<td width=100 height=80 align=center style='border: 1px solid #bcbcbc;";
                    if(($ru == $t_d) && ($s_Y == $t_Y) && ($s_m == $t_m)) echo "background:#FEFFC7;";
                    echo "'>";
                    if($ru<=0 || $ru>$s_t){ echo "&nbsp;"; } // 딱 그달에 맞는 숫자가 아님 표시하지 말자
                    else{
                        $s=date("Y-m-d",mktime(0,0,0,$s_m,$ru,$s_Y)); // 현재칸의 날짜
                        ?><a href='calender_result.html?cno=<?php echo $_GET['cno'];?>&cname=<?php echo $_GET['cname'];?>&bno=<?php echo $_GET['bno']?>&day=<?php echo $s;?>' <?php if(($ru == $t_d) && ($s_Y == $t_Y) && ($s_m == $t_m)) echo "style='color:red; font-weight:bold;'";?>><?
                        echo "$ru"; // 날짜입니다.
                       /* $query="SELECT * from subboard where cno='".$_GET['cno']."' and bno='".$_GET['bno']."' and date='".$s."'";
                        $result=mysql_query($query);
                        $row=mysql_fetch_object($result);
                        echo "</a><span style='margin-left:10px; display: inline-block; width: 65px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'><a href='schedule_read.html?cno=".$_GET['cno']."&cname=".$_GET['cname']."&bno=".$_GET['bno']."&sno=".$row->sno."&day=$s' style='color:black;'>";
                        if(mysql_num_rows($result)) {
                          echo $row->title;
                        }
                        echo "</a></span>";*/
                    }
                    echo "</td>";
                }
            echo "</tr>";
        }
        echo "</table>";
    }
    ?>
    <? crd($s); ?>
              <!--<td width=100 align=center><a href='schedule.html?cno=".$_GET['cno']."&cname=".$_GET['cname']."&bno=".$_GET['bno']."&s=$p_d'>◀</a></td>
              <td width=300 align=center colspan=3>$s_Y 년 $s_m 월</td>
              <td width=100 align=center><a href='schedule.html?cno=".$_GET['cno']."&cname=".$_GET['cname']."&bno=".$_GET['bno']."&s=$n_d'>▶</a></td>-->