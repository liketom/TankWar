# -*- coding:gbk -*-

import pygame
import sys
import traceback
import wall
import myTank
import enemyTank
import food

TankNum = 1  # ̹������

def main():
    pygame.init()
    pygame.mixer.init()

    resolution = 730, 630
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Tank War ")

    # ����ͼƬ,����,��Ч.
    background_image     = pygame.image.load(r"..\image\background.png")
    gameover_image       = pygame.image.load(r"..\image\gameover.png")
    home_destroyed_image = pygame.image.load(r"..\image\home_destroyed.png")

    bang_sound          = pygame.mixer.Sound(r"..\music\bang.wav")
    bang_sound.set_volume(1)
    fire_sound           = pygame.mixer.Sound(r"..\music\Gunfire.wav")
    start_sound          = pygame.mixer.Sound(r"..\music\start.wav")
    # start_sound.play()

    # ���徫����:̹�ˣ��ҷ�̹�ˣ��з�̹�ˣ��з��ӵ�
    allTankGroup     = pygame.sprite.Group()
    mytankGroup      = pygame.sprite.Group()
    allEnemyGroup    = pygame.sprite.Group()
    redEnemyGroup    = pygame.sprite.Group()
    greenEnemyGroup  = pygame.sprite.Group()
    otherEnemyGroup  = pygame.sprite.Group()
    enemyBulletGroup = pygame.sprite.Group()
    # ������ͼ
    bgMap = wall.Map()
    # ����ʳ��/���� ������ʾ
    prop = food.Food()
    # �����ҷ�̹��
    myTank_T1 = myTank.MyTank(1)
    allTankGroup.add(myTank_T1)
    mytankGroup.add(myTank_T1)
    if 1 == TankNum:
        myTank_T2 = myTank.MyTank(2)
        allTankGroup.add(myTank_T2)
        mytankGroup.add(myTank_T2)

    # �����з� ̹��
    for i in range(1, 4):
        enemy = enemyTank.EnemyTank(i)
        allTankGroup.add(enemy)
        allEnemyGroup.add(enemy)
        if enemy.isred == True:
            redEnemyGroup.add(enemy)
            continue
        if enemy.kind == 3:
            greenEnemyGroup.add(enemy)
            continue
        otherEnemyGroup.add(enemy)
    # �о�̹�˳��ֶ���
    appearance_image = pygame.image.load(r"..\image\appear.png").convert_alpha()
    appearance = []
    appearance.append(appearance_image.subsurface(( 0, 0), (48, 48)))
    appearance.append(appearance_image.subsurface((48, 0), (48, 48)))
    appearance.append(appearance_image.subsurface((96, 0), (48, 48)))




    # �Զ����¼�
    # �����з�̹���ӳ�200
    DELAYEVENT = pygame.constants.USEREVENT
    pygame.time.set_timer(DELAYEVENT, 200)
    # ���� �з� �ӵ��ӳ�1000
    ENEMYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 1
    pygame.time.set_timer(ENEMYBULLETNOTCOOLINGEVENT, 1000)
    # ���� �ҷ� �ӵ��ӳ�200
    MYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 2
    pygame.time.set_timer(MYBULLETNOTCOOLINGEVENT, 200)
    # �з�̹�� ��ֹ8000
    NOTMOVEEVENT = pygame.constants.USEREVENT + 3
    pygame.time.set_timer(NOTMOVEEVENT, 8000)


    delay = 100
    moving = 0
    movdir = 0
    moving2 = 0
    movdir2 = 0
    enemyNumber = 3
    enemyCouldMove      = True
    switch_R1_R2_image  = True
    homeSurvive         = True
    running_T1          = True
    running_T2          = True
    clock = pygame.time.Clock()
    while True:
        while not homeSurvive or not myTank_T1.life:
            screen.blit(home_destroyed_image, (3 + 12 * 24, 3 + 24 * 24))
            screen.blit(gameover_image, (3 + 12 * 24, 3 + 13 * 24))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()
                else:
                    continue
            pygame.display.flip()
            clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # �ҷ��ӵ���ȴ�¼�
            if event.type == MYBULLETNOTCOOLINGEVENT:
                myTank_T1.bulletNotCooling = True

            # �з��ӵ���ȴ�¼�
            if event.type == ENEMYBULLETNOTCOOLINGEVENT:
                for each in allEnemyGroup:
                    each.bulletNotCooling = True

            # �з�̹�˾�ֹ�¼�
            if event.type == NOTMOVEEVENT:
                enemyCouldMove = True

            # �����з�̹���ӳ�
            if event.type == DELAYEVENT:
                if enemyNumber < 4:
                    enemy = enemyTank.EnemyTank()
                    if pygame.sprite.spritecollide(enemy, allTankGroup, False, None):
                        break
                    allEnemyGroup.add(enemy)
                    allTankGroup.add(enemy)
                    enemyNumber += 1
                    if enemy.isred == True:
                        redEnemyGroup.add(enemy)
                    elif enemy.kind == 3:
                        greenEnemyGroup.add(enemy)
                    else:
                        otherEnemyGroup.add(enemy)

            if event.type == pygame.KEYDOWN:
                # print("key is %d" % event.key)
                if event.key == pygame.K_c and pygame.KMOD_CTRL:
                    pygame.quit()
                    sys.exit()

        # ����û��ļ��̲���
        key_pressed = pygame.key.get_pressed()
        # ���һ���ƶ�����
        if moving:
            moving -= 1
            if movdir == 0:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 1:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 2:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 3:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True

        if not moving:
            if key_pressed[pygame.K_w]:
                moving = 7
                movdir = 0
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_s]:
                moving = 7
                movdir = 1
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_a]:
                moving = 7
                movdir = 2
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_d]:
                moving = 7
                movdir = 3
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving = 0
                allTankGroup.add(myTank_T1)
        if key_pressed[pygame.K_j]:
            if not myTank_T1.bullet.life and myTank_T1.bulletNotCooling:
                # fire_sound.play()
                myTank_T1.shoot()
                myTank_T1.bulletNotCooling = False

        # ��Ҷ����ƶ�����
        if 1 != TankNum and moving2:
            moving2 -= 1
            if movdir2 == 0:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                running_T2 = True
            if movdir2 == 1:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                running_T2 = True
            if movdir2 == 2:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                running_T2 = True
            if movdir2 == 3:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                running_T2 = True

        if 1 != TankNum and not moving2:
            if key_pressed[pygame.K_UP]:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                moving2 = 7
                movdir2 = 0
                running_T2 = True
            elif key_pressed[pygame.K_DOWN]:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                moving2 = 7
                movdir2 = 1
                running_T2 = True
            elif key_pressed[pygame.K_LEFT]:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                moving2 = 7
                movdir2 = 2
                running_T2 = True
            elif key_pressed[pygame.K_RIGHT]:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                moving2 = 7
                movdir2 = 3
                running_T2 = True
        if 1 != TankNum and key_pressed[pygame.K_SPACE]:
            if not myTank_T2.bullet.life:
                # fire_sound.play()
                myTank_T2.shoot()


        # ��ɫ�����ػ�
        screen.fill((0, 0, 0))
        # ������
        screen.blit(background_image, (0, 0))
        # ��ש��
        for each in bgMap.brickGroup:
            screen.blit(each.image, each.rect)
        # ��ʯͷ
        for each in bgMap.ironGroup:
            screen.blit(each.image, each.rect)
        # ��home
        if homeSurvive:
            for each in bgMap.homeGroup:
                screen.blit(each.image, each.rect)

        # ��ʣ��������
        j = -1
        for i in range(myTank_T1.life):
            if 0 == i % 2:
                j += 1
                screen.blit(myTank_T1.tank_life, (27 * 24, 3 + (j * 32)))
            else:
                screen.blit(myTank_T1.tank_life, (30 + 27 * 24, 3 + (j * 32)))

        # ���ҷ�̹��1
        if not (delay % 5):
            switch_R1_R2_image = not switch_R1_R2_image
        if switch_R1_R2_image and running_T1:
            screen.blit(myTank_T1.tank_R0, (myTank_T1.rect.left, myTank_T1.rect.top))
            running_T1 = False
        else:
            screen.blit(myTank_T1.tank_R1, (myTank_T1.rect.left, myTank_T1.rect.top))

        # ���ҷ�̹��2
        if 1 != TankNum:
            if switch_R1_R2_image and running_T2:
                screen.blit(myTank_T2.tank_R0, (myTank_T2.rect.left, myTank_T2.rect.top))
                running_T2 = False
            else:
                screen.blit(myTank_T2.tank_R1, (myTank_T2.rect.left, myTank_T2.rect.top))

        # ���з�̹��
        for each in allEnemyGroup:
            # �ж�5ëǮ��Ч�Ƿ񲥷�
            if each.flash:
                #���жϻ����������Ҷ���
                if switch_R1_R2_image:
                    screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
                    if enemyCouldMove:
                        allTankGroup.remove(each)
                        each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(each)
                else:
                    screen.blit(each.tank_R1, (each.rect.left, each.rect.top))
                    if enemyCouldMove:
                        allTankGroup.remove(each)
                        each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(each)
            else:
                # ����5ëǮ��Ч
                if each.times > 0:
                    each.times -= 1
                    if each.times <= 10:
                        screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 20:
                        screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 30:
                        screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 40:
                        screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 50:
                        screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 60:
                        screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 70:
                        screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 80:
                        screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 90:
                        screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                if each.times == 0:
                    each.flash = True


        # �����ҷ��ӵ�1
        if myTank_T1.bullet.life:
            myTank_T1.bullet.move()
            screen.blit(myTank_T1.bullet.bullet, myTank_T1.bullet.rect)
            # �ӵ� ��ײ �ӵ�
            for each in enemyBulletGroup:
                if each.life:
                    if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                        myTank_T1.bullet.life = False
                        each.life = False
                        pygame.sprite.spritecollide(myTank_T1.bullet, enemyBulletGroup, True, None)
            # �ӵ� ��ײ �з�̹��
            if pygame.sprite.spritecollide(myTank_T1.bullet, redEnemyGroup, True, None):
                prop.change()
                # bang_sound.play()
                enemyNumber -= 1
                myTank_T1.bullet.life = False
            elif pygame.sprite.spritecollide(myTank_T1.bullet,greenEnemyGroup, False, None):
                for each in greenEnemyGroup:
                    if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                        if each.life == 1:
                            pygame.sprite.spritecollide(myTank_T1.bullet,greenEnemyGroup, True, None)
                            # bang_sound.play()
                            enemyNumber -= 1
                        elif each.life == 2:
                            each.life -= 1
                            each.tank = each.enemy_3_0
                        elif each.life == 3:
                            each.life -= 1
                            each.tank = each.enemy_3_2
                myTank_T1.bullet.life = False
            elif pygame.sprite.spritecollide(myTank_T1.bullet, otherEnemyGroup, True, None):
                # bang_sound.play()
                enemyNumber -= 1
                myTank_T1.bullet.life = False
            #if pygame.sprite.spritecollide(myTank_T1.bullet, allEnemyGroup, True, None):
            #    bang_sound.play()
            #    enemyNumber -= 1
            #    myTank_T1.bullet.life = False
            # �ӵ� ��ײ brickGroup
            if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.brickGroup, True, None):
                myTank_T1.bullet.life = False
            if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.homeGroup, True, None):
                myTank_T1.bullet.life = False
                homeSurvive = False
            # �ӵ� ��ײ ironGroup
            if myTank_T1.bullet.strong:
                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, True, None):
                    myTank_T1.bullet.life = False
            else:
                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, False, None):
                    myTank_T1.bullet.life = False

        # �����ҷ��ӵ�2
        if 1 != TankNum and myTank_T2.bullet.life:
            myTank_T2.bullet.move()
            screen.blit(myTank_T2.bullet.bullet, myTank_T2.bullet.rect)
            # �ӵ� ��ײ �з�̹��
            if pygame.sprite.spritecollide(myTank_T2.bullet, allEnemyGroup, True, None):
                # bang_sound.play()
                enemyNumber -= 1
                myTank_T2.bullet.life = False
            # �ӵ� ��ײ brickGroup
            if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.brickGroup, True, None):
                myTank_T2.bullet.life = False
                myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.homeGroup, True, None):
                myTank_T2.bullet.life = False
                homeSurvive = False
            # �ӵ� ��ײ brickGroup
            if myTank_T2.bullet.strong:
                if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.ironGroup, True, None):
                    myTank_T2.bullet.life = False
                    myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            else:
                if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.ironGroup, False, None):
                    myTank_T2.bullet.life = False
                    myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24


        # ���Ƶ����ӵ�
        for each in allEnemyGroup:
            # ����ӵ�û�������������ӵ�����
            if not each.bullet.life and each.bulletNotCooling and enemyCouldMove:
                enemyBulletGroup.remove(each.bullet)
                each.shoot()
                enemyBulletGroup.add(each.bullet)
                each.bulletNotCooling = False
            # ���5ëǮ��Ч������� ���� �ӵ���� ����Ƶз��ӵ�
            if each.flash:
                if each.bullet.life:
                    # ������˿����ƶ�
                    if enemyCouldMove:
                        each.bullet.move()
                    screen.blit(each.bullet.bullet, each.bullet.rect)
                    # �ӵ� ��ײ �ҷ�̹��
                    if pygame.sprite.collide_rect(each.bullet, myTank_T1):
                        myTank_T1.life -= 1
                        print("Tank1 life have", myTank_T1.life)
                        # bang_sound.play()
                        myTank_T1.rect.left, myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24
                        each.bullet.life = False
                        moving = 0  # �����ƶ����Ʋ���
                        for i in range(myTank_T1.level+1):
                            myTank_T1.levelDown()
                    if 1 != TankNum and pygame.sprite.collide_rect(each.bullet, myTank_T2):
                        # bang_sound.play()
                        myTank_T2.rect.left, myTank_T2.rect.top = 3 + 16 * 24, 3 + 24 * 24
                        each.bullet.life = False

                    if pygame.sprite.spritecollide(each.bullet, bgMap.homeGroup, True, None):
                        each.bullet.life = False
                        homeSurvive = False
                    # �ӵ� ��ײ brickGroup
                    if pygame.sprite.spritecollide(each.bullet, bgMap.brickGroup, True, None):
                        each.bullet.life = False
                    # �ӵ� ��ײ ironGroup
                    if each.bullet.strong:
                        if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, True, None):
                            each.bullet.life = False
                    else:
                        if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, False, None):
                            each.bullet.life = False

        # ���ʳ��/����
        if prop.life:
            screen.blit(prop.image, prop.rect)
            # �ҷ�̹����ײ ʳ��/����
            if pygame.sprite.collide_rect(myTank_T1, prop):
                if prop.kind == 1:  # ����ȫ��
                    for each in allEnemyGroup:
                        if pygame.sprite.spritecollide(each, allEnemyGroup, True, None):
                            # bang_sound.play()
                            enemyNumber -= 1
                    prop.life = False
                if prop.kind == 2:  # ���˾�ֹ
                    enemyCouldMove = False
                    prop.life = False
                if prop.kind == 3:  # �ӵ���ǿ
                    myTank_T1.bullet.strong = True
                    prop.life = False
                if prop.kind == 4:  # �ҵõ�����
                    for x, y in [(11,23),(12,23),(13,23),(14,23),(11,24),(14,24),(11,25),(14,25)]:
                        bgMap.iron = wall.Iron()
                        bgMap.iron.rect.left, bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                        bgMap.ironGroup.add(bgMap.iron)
                    prop.life = False
                if prop.kind == 5:  # ̹���޵�
                    prop.life = False
                    pass
                if prop.kind == 6:  # ̹������
                    myTank_T1.levelUp()
                    prop.life = False
                if prop.kind == 7:  # ̹������+1
                    myTank_T1.life += 1
                    prop.life = False




        # �ӳ�
        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
